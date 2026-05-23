# Cloud Cost Agent

Production-focused scaffold for a cloud cost optimization platform.

## Included foundations
- FastAPI backend with `/health` and dashboard summary endpoint.
- SQLAlchemy models + Alembic migration for initial persistence.
- Ports-and-adapters cloud interface with AWS Cost Explorer adapter.
- Detector plugin registry and initial idle compute detector.
- Celery task module structure for ingestion and analysis workflows.
- Frontend React dashboard components for KPI summary cards.
- CI pipeline (GitHub Actions) for lint/type-check/test stages.

## Local commands
- `make dev` to start local services with Docker Compose.
- `cd backend && python -m compileall app tests` for quick static sanity checks.
