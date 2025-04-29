import inject
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

# must import all models before calling create_all,
# so ignore unused import warnings here
# pylint: disable=W0611
from zimit_manager.models import ZimitExecution, ZimitTask  # noqa: F401

# black demands the space above, which is annoying
# pylint: enable=W0611


@inject.autoparams()
def create_db_and_tables(sqlite_url: str, echo_sql: bool) -> Engine:
    engine = create_engine(sqlite_url, echo=echo_sql)
    SQLModel.metadata.create_all(engine)
    return engine
