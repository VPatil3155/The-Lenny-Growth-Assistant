"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import get_settings
from .database import check_database_connection
from .health import router as health_router
from api.artifacts import router as artifacts_router
from api.messages import router as messages_router
from api.sessions import router as sessions_router


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Verify required infrastructure before serving requests."""

    check_database_connection()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(health_router)
app.include_router(artifacts_router)
app.include_router(sessions_router)
app.include_router(messages_router)
