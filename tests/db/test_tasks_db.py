from tests.factories import ZimitTaskFactory
from zimit_manager.db.tasks import create_task, get_task_by_id, get_tasks
from zimit_manager.models import ZimitTaskCreate


def test_create_task(factory_session):
    task_def = ZimitTaskCreate(
        name="mouse dance",
        requested_by="amy",
        short_name="mouse",
        url="http://mousedance.com",
    )

    task = create_task(factory_session, task_def)
    assert task is not None
    assert task.name == task_def.name
    assert task.urgency == task_def.urgency


def test_get_task_by_id(factory_session):
    task1 = ZimitTaskFactory.create(
        extra_hops=1,
        name="mouse dance!!!",
        short_name="dance",
        url="http://mousedance.com",
    )
    factory_session.flush()
    factory_session.refresh(task1)

    task2 = ZimitTaskFactory.create(
        extra_hops=1,
        name="hamster dance!!!",
        short_name="dance",
        url="http://hamsterdance.com",
    )
    factory_session.flush()
    factory_session.refresh(task2)

    assert get_task_by_id(factory_session, task1.id).name == "mouse dance!!!"
    assert get_task_by_id(factory_session, task2.id).name == "hamster dance!!!"
    assert get_task_by_id(factory_session, -4) is None


def test_get_tasks(factory_session):
    task1 = ZimitTaskFactory.create(
        extra_hops=1,
        name="mouse dance!!!",
        short_name="dance",
        url="http://mousedance.com",
    )
    factory_session.flush()
    factory_session.refresh(task1)

    task2 = ZimitTaskFactory.create(
        extra_hops=1,
        name="hamster dance!!!",
        short_name="dance",
        url="http://hamsterdance.com",
    )
    factory_session.flush()
    factory_session.refresh(task2)

    task_names = [task.name for task in get_tasks(factory_session)]
    assert len(task_names) == 2
    assert "mouse dance!!!" in task_names
    assert "hamster dance!!!" in task_names
