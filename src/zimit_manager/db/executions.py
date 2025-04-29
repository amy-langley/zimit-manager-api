from typing import Sequence

from sqlmodel import Session, select

from zimit_manager.enums import ExecutionStatus
from zimit_manager.models import ZimitExecution, ZimitExecutionCreate


def create_execution(
    session: Session, execution: ZimitExecutionCreate
) -> ZimitExecution:
    new_execution = ZimitExecution.model_validate(execution)
    new_execution.status = ExecutionStatus.PROCESSING
    session.add(new_execution)
    session.flush()
    session.refresh(new_execution)
    return new_execution


def get_execution_by_id(
    session: Session,
    execution_id: int,
) -> ZimitExecution | None:
    return session.get(ZimitExecution, execution_id)


def get_executions(session: Session) -> Sequence[ZimitExecution]:
    return session.exec(select(ZimitExecution)).all()
