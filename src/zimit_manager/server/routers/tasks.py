from environs import env
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from sqlmodel import Session

from zimit_manager import db
from zimit_manager.db.executions import create_execution
from zimit_manager.models import (
    ZimitExecutionAPI,
    ZimitExecutionCreate,
    ZimitTaskAPI,
    ZimitTaskAPIWithExecutions,
    ZimitTaskCreate,
)
from zimit_manager.server.util import get_session
from zimit_manager.services import zimit_service

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("", response_model=ZimitTaskAPI)
def create_task(
    *, session: Session = Depends(get_session), task_contents: ZimitTaskCreate
):
    return db.tasks.create_task(session, task_contents)


@router.get("", response_model=list[ZimitTaskAPI])
def get_tasks(*, session: Session = Depends(get_session)):
    return db.tasks.get_tasks(session)


@router.get("/{task_id}", response_model=ZimitTaskAPIWithExecutions)
def get_task(*, session: Session = Depends(get_session), task_id: int):
    task = db.tasks.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/{task_id}/launch", status_code=202)
def launch_task(
    *,
    background_tasks: BackgroundTasks,
    response: Response,
    session: Session = Depends(get_session),
    task_id: int,
) -> int:
    # TODO: this is too much logic to put into a controller, break
    # it up into some methods on zimit service probably
    task = db.tasks.get_task_by_id(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    execution_def = ZimitExecutionCreate(
        output_dir=env.str("DEFAULT_OUTPUT_DIR"),
        task_id=task.id,
    )

    new_execution = ZimitExecutionAPI.model_validate(
        create_execution(session, execution_def)
    )
    background_tasks.add_task(zimit_service.launch_execution, session, new_execution.id)
    response.status_code = status.HTTP_202_ACCEPTED
    return new_execution.id
