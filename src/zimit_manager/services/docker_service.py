import json
from typing import Callable, Dict, List

import docker
from docker.models.containers import Container


def run_attached(
    container_image: str, container_command: str | List[str], **kwargs
) -> str:
    client = docker.from_env()
    return str(client.containers.run(container_image, container_command, **kwargs))


def run_detached(
    container_image: str, container_comannd: str | List[str], **kwargs
) -> Container:
    client = docker.from_env()
    return client.containers.run(
        container_image, container_comannd, **{**kwargs, "detach": True}
    )


def get_logs(
    container_name_or_id: str,
    lines: int = 0,
    log_filter: Callable[[str], bool] = lambda _: True,
) -> List[Dict]:
    client = docker.from_env()
    container = client.containers.get(container_name_or_id)

    return [
        json.loads(line)
        for line in container.logs(tail=lines if lines > 0 else "all")
        .decode("utf-8")
        .split("\n")
        if log_filter(line)
    ]
