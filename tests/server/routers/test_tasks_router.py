from fastapi import FastAPI
from fastapi.testclient import TestClient

from tests.factories import ZimitTaskFactory
from zimit_manager.models import ZimitTaskAPI
from zimit_manager.server.routers.tasks import router as task_router


def test_endpoint(factory_session, mocker):
    # note: mocker automatically employs a context manager
    # so we can just use this naively
    mocked_get_session = mocker.patch("zimit_manager.server.util.session_getter")
    mocked_get_session.return_value = factory_session

    app = FastAPI()
    app.include_router(task_router)

    example_task = ZimitTaskFactory.create(
        description="my task",
        url="http://hamsterdance.com",
    )
    factory_session.flush()
    factory_session.refresh(example_task)

    client = TestClient(app)
    response = client.get("/tasks")
    assert response.status_code == 200

    tasks = [ZimitTaskAPI(**task) for task in response.json()]

    assert len(tasks) == 1
    assert isinstance(tasks[0], ZimitTaskAPI)
    assert tasks[0].url == "http://hamsterdance.com"
