import copy
import importlib
import json
import os
import sys
import traceback
import zlib
from datetime import datetime
from io import StringIO

from dotenv import load_dotenv
from pydantic import ValidationError
from redis import Redis

from dropbase.helpers.logger import update_dev_logs
from dropbase.helpers.state_handler import get_changed_values, state_to_dict

load_dotenv()


def run(r: Redis):

    task_id = os.getenv("job_id")
    response = {
        "id": task_id,
        "stdout": "",
        "traceback": "",
        "message": "",
        "type": "",
        "status_code": 202,
    }

    new_state = {}

    try:

        # redirect stdout
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output

        # read state and context
        app_name = os.getenv("app_name")
        page_name = os.getenv("page_name")

        # get page module
        page_path = f"workspace.{app_name}.{page_name}"
        state_context_module = importlib.import_module(page_path)

        # initialize state
        state = json.loads(os.getenv("state"))
        State = getattr(state_context_module, "State")
        state = State(**state)

        # initialize page script
        script_path = f"workspace.{app_name}.{page_name}.functions"
        functions_module = importlib.import_module(script_path)
        importlib.reload(functions_module)
        action = getattr(functions_module, os.getenv("action"))

        in_state = copy.deepcopy(state)
        out_state = action(in_state)

        if isinstance(out_state, State):

            # assert out_state is a State object
            State(**out_state.model_dump())

            new_state = get_changed_values(state, out_state)

            response["type"] = "state"
            response["message"] = "Job completed"
            response["status_code"] = 200
            response["state"] = state_to_dict(new_state)
        else:
            response["type"] = "error"
            message = f'Make sure {os.getenv("action")} function returns a state object'
            message += f'\n{os.getenv("action")} returned: {type(out_state)}'
            response["message"] = message
            response["status_code"] = 500
    except TypeError as e:
        # catch type errors and send to redis
        response["type"] = "error"
        response["message"] = "TypeError: " + str(e) + "\nMake sure the function returns a state object"
        response["status_code"] = 500
        response["traceback"] = traceback.format_exc()
    except ValidationError as e:
        # catch validation errors and send to redis
        response["type"] = "error"
        response["message"] = "ValidationError: " + str(e) + "\nConfirm the state returned is valid"
        response["status_code"] = 500
        response["traceback"] = traceback.format_exc()
    except Exception as e:
        # catch any error and tracebacks and send to redis
        response["type"] = "error"
        response["message"] = str(e)
        response["status_code"] = 500
        response["traceback"] = traceback.format_exc()
    finally:
        # get stdout
        response["stdout"] = redirected_output.getvalue()
        sys.stdout = old_stdout

        # update redis with the response
        job_id = os.getenv("job_id")
        data = json.dumps(response, default=str, separators=(",", ":"))
        if r.hget(job_id, "status") == b"202":
            r.hset(job_id, mapping={"status": response["status_code"], "data": data})
            r.expire(job_id, 60)

        # log to dev logs
        # NOTE: we're logging the state_out, stdout, and traceback as compressed bytes
        # so we need to compress them before sending them to the database
        response["completed_at"] = int(datetime.now().timestamp())
        state_json = json.dumps(new_state, default=str, separators=(",", ":"))
        response["state_out"] = zlib.compress(state_json.encode("utf-8"))
        response["stdout"] = zlib.compress(response["stdout"].encode("utf-8"))
        response["traceback"] = zlib.compress(response["traceback"].encode("utf-8"))
        update_dev_logs(response)
