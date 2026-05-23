"""Background jobs for ingestion and detection loops."""

from celery.utils.log import get_task_logger

from app.detectors.base import DetectorRegistry
from app.detectors.idle_compute import IdleComputeDetector

logger = get_task_logger(__name__)
registry = DetectorRegistry()
registry.register(IdleComputeDetector())


def ingest_costs() -> dict:
    logger.info("cost_ingestion_started")
    return {"status": "ok", "ingested": 0}


def run_detectors(resources: list[dict], metrics: dict[str, dict]) -> dict:
    finding_count = 0
    for detector in registry.all():
        finding_count += len(detector.detect(resources, metrics))
    logger.info("detectors_completed", findings=finding_count)
    return {"status": "ok", "findings": finding_count}
