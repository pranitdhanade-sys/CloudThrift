"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-23
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cloud_accounts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.Enum("AWS", "GCP", "AZURE", name="provider"), nullable=False),
        sa.Column("account_id", sa.String(length=128), nullable=False, unique=True),
        sa.Column("alias", sa.String(length=255), nullable=False),
        sa.Column("credentials_ref", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
    )
    op.create_table(
        "cost_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey("cloud_accounts.id"), nullable=False),
        sa.Column("service", sa.String(length=255), nullable=False),
        sa.Column("region", sa.String(length=128), nullable=False),
        sa.Column("resource_id", sa.String(length=255), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("amount_usd", sa.Numeric(12, 4), nullable=False),
        sa.Column("currency", sa.String(length=16), nullable=False),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("cost_records")
    op.drop_table("cloud_accounts")
