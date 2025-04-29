from tests.factories import ZimitExecutionFactory, ZimitTaskFactory


def test_relationship(factory_session):  # pylint:disable=unused-argument
    example_task = ZimitTaskFactory.create(
        description="my task",
        url="http://hamsterdance.com",
    )
    factory_session.flush()
    factory_session.refresh(example_task)

    executions = ZimitExecutionFactory.create_batch(3, task_id=example_task.id)
    factory_session.flush()

    for execution in executions:
        factory_session.refresh(execution)
        assert execution.task.id == example_task.id

    factory_session.refresh(example_task)
    assert len(example_task.executions) == 3
