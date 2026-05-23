"""Celery app factory with resilient defaults for retries and routing."""

from celery import Celery

celery_app = Celery("cloud_cost_agent", broker="redis://redis:6379/0", backend="redis://redis:6379/1")
celery_app.conf.task_acks_late = True
celery_app.conf.task_default_retry_delay = 30
celery_app.conf.task_routes = {
    "app.tasks.jobs.ingest_costs": {"queue": "ingestion"},
    "app.tasks.jobs.run_detectors": {"queue": "analysis"},
}
