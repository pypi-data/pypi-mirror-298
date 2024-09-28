import json
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text


def update_dev_logs(records: dict):
    try:
        connection_str = _get_connection_string()
        engine = create_engine(connection_str)
        with engine.begin() as connection:
            sql = """
            UPDATE task
            SET
                state_out = :state_out,
                stdout = :stdout,
                traceback = :traceback,
                message = :message,
                type = :type,
                completed_at = :completed_at
            WHERE id = :id;
            """  # noqa
            connection.execute(text(sql), records)
        engine.dispose()
    except SQLAlchemyError as e:
        print(f"Failed to execute log record query: {e}")
        raise e


def _get_connection_string():
    dev_db = os.getenv("dev_db")
    if dev_db and isinstance(dev_db, str):
        dev_db = json.loads(dev_db)
        if "postgres" in dev_db.get("drivername"):
            return URL.create(
                drivername=dev_db.get("drivername"),
                username=dev_db.get("username"),
                password=dev_db.get("password"),
                host=dev_db.get("host"),
                port=dev_db.get("port") or 5432,
                database=dev_db.get("database"),
            )
        elif "sqlite" in dev_db.get("drivername"):
            return f"sqlite:///{dev_db['host']}"
        else:
            raise ValueError("Invalid database type")
    else:
        return "sqlite:///files/dev.db"
