"""Primary SQLAlchemy models for accounts, costs, findings, and recommendations."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SAEnum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Provider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class FindingStatus(str, Enum):
    OPEN = "open"
    SNOOZED = "snoozed"
    RESOLVED = "resolved"


class CloudAccount(Base):
    """Connected cloud account metadata."""

    __tablename__ = "cloud_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[Provider] = mapped_column(SAEnum(Provider), nullable=False)
    account_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    alias: Mapped[str] = mapped_column(String(255), nullable=False)
    credentials_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")


class CostRecord(Base):
    """Normalized daily cost records by resource/service."""

    __tablename__ = "cost_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("cloud_accounts.id"), nullable=False)
    service: Mapped[str] = mapped_column(String(255), nullable=False)
    region: Mapped[str] = mapped_column(String(128), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    amount_usd: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(16), nullable=False, default="USD")
    tags: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)


class WasteFinding(Base):
    """Detected waste candidates with evidence payload."""

    __tablename__ = "waste_findings"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("cloud_accounts.id"), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(255), nullable=False)
    detector_name: Mapped[str] = mapped_column(String(128), nullable=False)
    estimated_savings: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False)
    confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), nullable=False)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[FindingStatus] = mapped_column(SAEnum(FindingStatus), nullable=False, default=FindingStatus.OPEN)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


class Recommendation(Base):
    """LLM-generated recommendation bundles for one or more findings."""

    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    finding_ids: Mapped[list[int]] = mapped_column(ARRAY(String), nullable=False)
    summary: Mapped[str] = mapped_column(String(500), nullable=False)
    rationale: Mapped[str] = mapped_column(String(4000), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    remediation_steps: Mapped[dict] = mapped_column(JSONB, nullable=False)
    claude_thread_id: Mapped[str] = mapped_column(String(255), nullable=False)
    engineer_feedback: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="proposed")


class RemediationAction(Base):
    """Audit record for remediation executions and dry-run operations."""

    __tablename__ = "remediation_actions"

    id: Mapped[int] = mapped_column(primary_key=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey("recommendations.id"), nullable=False)
    dry_run: Mapped[bool] = mapped_column(nullable=False, default=True)
    approver_id: Mapped[str] = mapped_column(String(255), nullable=True)
    executed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    result: Mapped[dict] = mapped_column(JSONB, nullable=False)
    cost_delta: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False, default=0)
