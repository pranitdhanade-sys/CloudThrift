from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_summary_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200
    body = response.json()
    assert "mtd_spend" in body
    assert "identified_savings" in body
