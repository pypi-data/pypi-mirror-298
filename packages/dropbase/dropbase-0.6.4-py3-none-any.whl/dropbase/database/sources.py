import logging

from pydantic import ValidationError

from dropbase.database.schemas import MySQLCreds, PgCreds, SnowflakeCreds, SqliteCreds
from dropbase.helpers.config import load_toml

db_type_to_class = {
    "postgres": PgCreds,
    "pg": PgCreds,
    "mysql": MySQLCreds,
    "sqlite": SqliteCreds,
    "snowflake": SnowflakeCreds,
}

worker_envs = load_toml("workspace/worker.toml")


def get_sources():
    # get sources from toml file
    databases = worker_envs.get("database", {})

    sources = {}
    for db_type in databases:
        for name, creds in databases[db_type].items():
            try:
                # in this step, we both validate and ingest additional fields to the creds
                SourceClass = db_type_to_class.get(db_type)
                creds = SourceClass(**creds)
                # add to sources
                sources[name] = {"creds": creds.dict(), "type": db_type}
            except ValidationError as e:
                logging.warning(f"Failed to validate source {name}.\n\nError: " + str(e))
    return sources
