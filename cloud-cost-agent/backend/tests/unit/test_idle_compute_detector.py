from app.detectors.idle_compute import IdleComputeDetector


def test_idle_compute_detector_finds_underutilized_instances() -> None:
    detector = IdleComputeDetector()
    resources = [{"resource_id": "i-123", "type": "ec2"}, {"resource_id": "i-999", "type": "ec2"}]
    metrics = {
        "i-123": {"cpu_avg": 2.1, "monthly_cost": 84.0, "days": 14, "in_asg": False},
        "i-999": {"cpu_avg": 44.0, "monthly_cost": 220.0, "days": 14, "in_asg": False},
    }

    findings = detector.detect(resources, metrics)

    assert len(findings) == 1
    assert findings[0].resource_id == "i-123"
    assert findings[0].estimated_monthly_savings == 84.0
