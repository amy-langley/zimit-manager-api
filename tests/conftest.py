import functools
import inspect
import tempfile

import inject
import pytest
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel

from tests import factories
from zimit_manager.db.core import create_db_and_tables

# enumerate every actual factory in factories.py
ENUMERATED_FACTORIES = [
    c
    for c in [
        a for a in [getattr(factories, f) for f in dir(factories)] if inspect.isclass(a)
    ]
    if issubclass(c, SQLAlchemyModelFactory) and c is not SQLAlchemyModelFactory
]


@pytest.fixture(scope="function")
def fake_engine():
    with tempfile.NamedTemporaryFile(suffix="db") as tempdb:
        engine = create_db_and_tables(
            f"sqlite:///{tempdb.name}",
            False,
        )
        yield engine


@pytest.fixture(scope="function")
def fake_session(fake_engine):  # pylint:disable=W0621
    with Session(fake_engine) as session:
        inject.clear_and_configure(
            functools.partial(tests_binder, engine=fake_engine, session=session)
        )
        yield session

    if isinstance(fake_engine, Engine):
        SQLModel.metadata.drop_all(fake_engine)


@pytest.fixture(scope="function")
def factory_session(fake_session):  # pylint:disable=W0621
    for factory in ENUMERATED_FACTORIES:
        factory._meta.sqlalchemy_session = fake_session  # pylint:disable=W0212

    yield fake_session

    fake_session.rollback()


def tests_binder(binder, *, engine, session):
    binder.bind(Engine, engine)
    binder.bind(Session, session)
