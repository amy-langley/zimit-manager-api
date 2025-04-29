from docker.models.containers import Container

from zimit_manager.services.docker_service import run_detached


def test_run_detached():
    container: Container  # type: ignore  # shut up mypy
    try:
        container = run_detached("hello-world", [])
        assert isinstance(container, Container)

        exit_code = container.wait(timeout=30)
        assert exit_code["StatusCode"] == 0

        output = str(container.logs())
        assert "Hello from Docker" in output
    finally:
        container.remove(force=True)
