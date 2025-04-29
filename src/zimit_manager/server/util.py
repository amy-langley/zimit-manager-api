import inject
from sqlalchemy import Engine
from sqlmodel import Session


def get_session():
    with session_getter() as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


# mock this function to test the api in the unit tests
# why is this a separate function? because FastAPI has worms in its brain
@inject.autoparams()
def session_getter(engine: Engine = None):
    return Session(engine)
