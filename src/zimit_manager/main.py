from zimit_manager.server.core import configure_server
from zimit_manager.server.routers import executions, tasks

app = configure_server()
app.include_router(executions.router)
app.include_router(tasks.router)
