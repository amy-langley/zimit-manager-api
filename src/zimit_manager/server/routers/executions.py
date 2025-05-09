from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from zimit_manager import db
from zimit_manager.models import (
    ZimitExecutionAPI,
    ZimitExecutionAPIWithTask,
    ZimitExecutionProgress,
)
from zimit_manager.server.util import get_session
from zimit_manager.services.zimit_service import get_progress

router = APIRouter(
    prefix="/executions",
    tags=["executions"],
)


@router.get("", response_model=list[ZimitExecutionAPI])
def get_executions(session: Session = Depends(get_session)):
    return db.executions.get_executions(session)


@router.get("/{execution_id}", response_model=ZimitExecutionAPIWithTask)
def get_execution(*, session: Session = Depends(get_session), execution_id: int):
    execution = db.executions.get_execution_by_id(session, execution_id)
    if execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")

    return execution


@router.get("/{execution_id}/progress", response_model=ZimitExecutionProgress)
def get_execution_progress(
    *, session: Session = Depends(get_session), execution_id: int
):
    return get_progress(session, execution_id)
