from typing import Sequence

from sqlmodel import Session, select

from zimit_manager.models import ZimitTask, ZimitTaskCreate


def create_task(session: Session, task: ZimitTaskCreate) -> ZimitTask:
    db_task = ZimitTask.model_validate(task)
    session.add(db_task)
    session.flush()  # do not commit! only have to flush to get id
    session.refresh(db_task)
    return db_task


def get_task_by_id(
    session: Session,
    task_id: int,
) -> ZimitTask | None:
    return session.get(ZimitTask, task_id)


def get_tasks(session: Session) -> Sequence[ZimitTask]:
    return session.exec(select(ZimitTask)).all()
