from tests.factories import ZimitExecutionFactory, ZimitTaskFactory
from zimit_manager.db.executions import (
    create_execution,
    get_execution_by_id,
    get_executions,
)
from zimit_manager.models import ZimitExecutionCreate


def test_create_execution(factory_session):
    task = ZimitTaskFactory.create(
        extra_hops=1,
        name="mouse dance!!!",
        short_name="dance",
        url="http://mousedance.com",
    )
    factory_session.flush()
    factory_session.refresh(task)

    execution_def = ZimitExecutionCreate(
        memory="2g",
        output_dir="/tmp/foo",
        task_id=task.id,
        workers=4,
    )

    execution = create_execution(factory_session, execution_def)

    factory_session.refresh(task)

    assert execution.memory == "2g"
    assert execution.task_id == task.id

    assert execution.task is not None
    assert execution.task.name == "mouse dance!!!"

    assert task.executions is not None
    assert len(task.executions) == 1
    assert task.executions[0].memory == "2g"


def test_get_execution_by_id(factory_session):
    new_task = ZimitTaskFactory.create(
        extra_hops=1,
        name="mouse dance!!!",
        short_name="dance",
        url="http://mousedance.com",
    )
    factory_session.flush()
    factory_session.refresh(new_task)

    new_execution = ZimitExecutionFactory.create(
        memory="2g",
        task_id=new_task.id,
        workers=4,
    )
    factory_session.flush()
    factory_session.refresh(new_execution)

    execution = get_execution_by_id(factory_session, new_execution.id)
    assert execution.id == new_execution.id
    assert execution.task_id == new_task.id
    assert execution.memory == "2g"


def test_get_executions(factory_session):
    new_task = ZimitTaskFactory.create(
        extra_hops=1,
        name="mouse dance!!!",
        short_name="dance",
        url="http://mousedance.com",
    )
    factory_session.flush()
    factory_session.refresh(new_task)

    new_execution1 = ZimitExecutionFactory.create(
        memory="2g",
        task_id=new_task.id,
        workers=4,
    )
    factory_session.flush()
    factory_session.refresh(new_execution1)

    new_execution2 = ZimitExecutionFactory.create(
        memory="8g",
        task_id=new_task.id,
        workers=16,
    )
    factory_session.flush()
    factory_session.refresh(new_execution2)

    executions = get_executions(factory_session)
    assert executions is not None
    assert len(executions) == 2

    for execution in executions:
        assert execution.task_id == new_task.id

    memories = [execution.memory for execution in executions]
    assert "2g" in memories
    assert "8g" in memories
