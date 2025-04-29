import datetime
from tempfile import TemporaryDirectory

from tests.factories import ZimitExecutionFactory, ZimitTaskFactory
from zimit_manager.db.executions import create_execution
from zimit_manager.enums import ExecutionStatus, ScopeType
from zimit_manager.models import ZimitExecutionCreate
from zimit_manager.services.zimit_service import (
    generate_docker_params,
    generate_zimit_params,
    launch_execution,
)


def test_docker_params(factory_session):  # pylint:disable-unused-argument
    example_task = ZimitTaskFactory.create(
        extra_hops=1,
        name="Mouse Dance!!!",
        short_name="dance",
        scope_type=ScopeType.DOMAIN,
        url="http://mousedance.com",
    )
    factory_session.flush()
    factory_session.refresh(example_task)

    example_execution = ZimitExecutionFactory.create(
        memory="2g",
        task_id=example_task.id,
        workers=4,
    )
    factory_session.flush()
    factory_session.refresh(example_execution)

    params = generate_docker_params(example_execution)
    assert len(params) > 0
    assert params["mem_limit"] == "2g"
    assert params["name"] == "zimit-dance"


def test_generate_zimit_params(factory_session):  # pylint:disable=unused-argument
    example_task = ZimitTaskFactory.create(
        extra_hops=1,
        name="Mouse Dance!!!",
        scope_type=ScopeType.DOMAIN,
        url="http://mousedance.com",
    )
    factory_session.flush()
    factory_session.refresh(example_task)

    example_execution = ZimitExecutionFactory.create(
        memory="2g",
        task_id=example_task.id,
        workers=4,
    )
    factory_session.flush()
    factory_session.refresh(example_execution)

    param_text = generate_zimit_params(example_execution)
    assert "--name mouse-dance" in param_text
    assert "--extraHops 1" in param_text
    assert "--scopeType domain" in param_text
    assert "--workers 4" in param_text


def test_launch_task(factory_session):  # pylint:disable-unused-argument
    with TemporaryDirectory() as tmpdir:
        example_task = ZimitTaskFactory.create(
            extra_hops=1,
            name="Mouse Dance!!!",
            short_name="dance",
            scope_type=ScopeType.DOMAIN,
            url="http://mousedance.com",
        )
        factory_session.flush()
        factory_session.refresh(example_task)

        # new_execution = create_execution(factory_session, example_task.id, tmpdir)
        execution_def = ZimitExecutionCreate(
            output_dir=tmpdir,
            task_id=example_task.id,
        )
        new_execution = create_execution(factory_session, execution_def)

        result = launch_execution(factory_session, new_execution.id, "hello-world", "")

        assert result.container_id is not None
        assert result.output_dir == tmpdir
        assert result.status == ExecutionStatus.PROCESSING

        # the database dates are timezone-naive
        now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        assert (now - result.started).seconds < 10
