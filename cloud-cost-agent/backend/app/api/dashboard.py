"""Dashboard API endpoints for UI summary widgets."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary() -> dict:
    return {
        "mtd_spend": 12456.44,
        "mom_change_pct": -8.2,
        "forecast_30d": 35789.0,
        "identified_savings": 5120.0,
    }
