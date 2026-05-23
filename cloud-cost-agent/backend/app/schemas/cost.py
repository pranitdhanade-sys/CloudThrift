"""Pydantic schemas for normalized cost and waste finding payloads."""

from datetime import date

from pydantic import BaseModel, Field


class CostRecordIn(BaseModel):
    account_id: int
    service: str
    region: str
    resource_id: str
    date: date
    amount_usd: float = Field(ge=0)
    currency: str = "USD"
    tags: dict[str, str] = Field(default_factory=dict)


class WasteFindingOut(BaseModel):
    resource_id: str
    waste_type: str
    estimated_monthly_savings: float
    confidence_score: float = Field(ge=0, le=1)
    evidence_data: dict
