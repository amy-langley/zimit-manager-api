from typing import Any, Dict

from sqlmodel import Session

from zimit_manager.db.executions import get_execution_by_id
from zimit_manager.exceptions import MissingZimitExecution, ZimitExecutionNotRunning
from zimit_manager.models import ZimitExecution, ZimitExecutionProgress
from zimit_manager.services.docker_service import get_logs, run_detached

ZIMIT_IMAGE_NAME = "ghcr.io/openzim/zimit"
ZIMIT_COMMAND_NAME = "zimit"


def generate_docker_params(execution: ZimitExecution) -> Dict[str, Any]:
    task = execution.task
    if task is None:
        raise ValueError("No task associated with this execution")

    return {
        "detach": True,
        "mem_limit": execution.memory,
        "name": f"zimit-{task.short_name.lower()}",
        "auto_remove": True,
        "volumes": {
            execution.output_dir: {
                "bind": "/output",
                "mode": "rw",
            }
        },
    }


def generate_zimit_params(execution: ZimitExecution) -> str:
    task = execution.task

    if task is None:
        raise ValueError("No task associated with this execution")

    kebab = "-".join(
        "".join(c for c in chunk if c.isalnum()) for chunk in task.name.lower().split()
    )

    return " ".join(
        [
            f'--desc "{task.description}"',
            f"--extraHops {task.extra_hops}",
            f"--lang {task.language}",
            "--logLevel info,log,warn,warning,error,fatal",
            f"--name {kebab}",
            f"--scopeType {task.scope_type.name.lower()}",
            f'--seeds "{task.url}"',
            f'--title "{task.name}"',
            f"--workers {execution.workers}",
        ]
    )


def launch_execution(
    session: Session,
    execution_id: int,
    image_name: str = ZIMIT_IMAGE_NAME,
    command_name: str = ZIMIT_COMMAND_NAME,
) -> ZimitExecution:
    execution = get_execution_by_id(session, execution_id)

    if execution is None:
        raise MissingZimitExecution(f"No execution id found with id {execution_id}")

    docker_params = generate_docker_params(execution)
    zimit_params = generate_zimit_params(execution)

    command_text = ""
    if command_name:
        if zimit_params:
            command_text = f"{command_name} {zimit_params}"
        else:
            command_text = command_name

    print(f"starting run detached for {execution}")
    container = run_detached(image_name, command_text, **docker_params)
    execution.container_id = container.id
    session.flush()

    return execution


def get_progress(session: Session, execution_id: int) -> ZimitExecutionProgress:
    execution = get_execution_by_id(session, execution_id)

    if execution is None:
        raise MissingZimitExecution(f"Could not find execution {execution_id}")

    if execution.container_id is None:
        raise ZimitExecutionNotRunning(f"No active container for {execution_id}")

    params = {
        **{
            k: v
            for k, v in (
                get_logs(
                    execution.container_id, 20, lambda line: "statistic" in line.lower()
                )
            )[-1].items()
            if k in ZimitExecutionProgress.model_fields.keys()
        },
        "container_id": execution.container_id,
    }

    return ZimitExecutionProgress(**params)
