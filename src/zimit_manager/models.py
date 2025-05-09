import datetime

from sqlmodel import Field, Relationship, SQLModel

from zimit_manager.enums import ExecutionStatus, ScopeType, Urgency


class ZimitTaskBase(SQLModel):
    description: str | None = Field(default=None)
    extra_hops: int = Field(default=0)
    language: str = Field(default="eng")
    name: str
    requested_by: str
    scope_type: ScopeType = Field(default=ScopeType.DOMAIN)
    short_name: str
    urgency: Urgency = Field(default=Urgency.SAFE)
    url: str


class ZimitTaskCreate(ZimitTaskBase):
    pass


class ZimitTask(ZimitTaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    executions: list["ZimitExecution"] = Relationship(back_populates="task")


class ZimitTaskAPI(ZimitTaskBase):
    id: int


class ZimitExecutionBase(SQLModel):
    memory: str = Field(default="4g")
    output_dir: str
    task_id: int = Field(foreign_key="zimittask.id")
    workers: int = Field(default=6)


class ZimitExecutionCreate(ZimitExecutionBase):
    pass


class ZimitExecution(ZimitExecutionBase, table=True):
    container_id: str | None = Field(default=None)
    id: int | None = Field(default=None, primary_key=True)
    result_link: str | None = Field(default=None)
    started: datetime.datetime = Field(default=datetime.datetime.now(datetime.UTC))
    status: ExecutionStatus = Field(default=ExecutionStatus.PROCESSING)
    task: ZimitTask | None = Relationship(back_populates="executions")


class ZimitExecutionAPI(ZimitExecutionBase):
    container_id: str | None
    id: int
    result_link: str | None
    started: datetime.datetime = Field(default=datetime.datetime.now(datetime.UTC))
    status: ExecutionStatus = Field(default=ExecutionStatus.PROCESSING)


class ZimitExecutionProgress(SQLModel):
    container_id: str
    crawled: int
    pending: int
    failed: int


class ZimitTaskAPIWithExecutions(ZimitTaskAPI):
    executions: list[ZimitExecutionAPI] = []


class ZimitExecutionAPIWithTask(ZimitExecutionAPI):
    task: ZimitTaskAPI | None = None
