"""FastAPI entrypoint exposing health and baseline API metadata."""

from fastapi import FastAPI

from app.api.dashboard import router as dashboard_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(dashboard_router)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "environment": settings.environment,
        "services": {"db": "up", "redis": "up", "adapters": "degraded"},
    }
