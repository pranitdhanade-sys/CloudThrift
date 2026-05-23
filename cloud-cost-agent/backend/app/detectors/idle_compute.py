"""Idle compute detector implementation."""

from app.detectors.base import WasteDetector
from app.schemas.cost import WasteFindingOut


class IdleComputeDetector(WasteDetector):
    name = "idle_compute"

    def detect(self, resources: list[dict], metrics: dict[str, dict]) -> list[WasteFindingOut]:
        findings: list[WasteFindingOut] = []
        for resource in resources:
            if resource.get("type") not in {"ec2", "vm"}:
                continue
            utilization = metrics.get(resource["resource_id"], {})
            cpu_avg = utilization.get("cpu_avg", 100)
            in_asg = utilization.get("in_asg", False)
            if cpu_avg < 5 and not in_asg:
                findings.append(
                    WasteFindingOut(
                        resource_id=resource["resource_id"],
                        waste_type="idle_compute",
                        estimated_monthly_savings=float(utilization.get("monthly_cost", 0)),
                        confidence_score=0.92,
                        evidence_data={"cpu_avg": cpu_avg, "days": utilization.get("days", 14)},
                    )
                )
        return findings
