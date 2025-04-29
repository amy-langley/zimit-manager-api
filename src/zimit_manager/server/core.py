import functools

import inject
from environs import env
from fastapi import FastAPI
from inject import Binder
from sqlalchemy import Engine

from zimit_manager.db.core import create_db_and_tables


# not much to inject yet, but just wait
def configure_injector(binder: Binder, *, engine):
    binder.bind(Engine, engine)


# this takes the place of the FastAPI lifecycle; we are not
# using lifecycle here to set up the injector because that
# is an async context handler and will occur too late
def configure_server() -> FastAPI:
    env.read_env()

    sqlite_url = f"sqlite:///{env.str('SQLITE_FILENAME', 'database.db')}"
    echo_sql = env.bool("ECHO_SQL", True)

    engine = create_db_and_tables(sqlite_url, echo_sql)

    inject.configure(functools.partial(configure_injector, engine=engine))

    return FastAPI()
