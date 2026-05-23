"""AWS adapter implementation using Cost Explorer and related service clients."""

from datetime import date

import boto3

from app.adapters.base import CloudAdapter


class AWSCloudAdapter(CloudAdapter):
    """AWS implementation of cloud adapter interface."""

    def __init__(self, region: str = "us-east-1") -> None:
        self.session = boto3.Session(region_name=region)
        self.cost_explorer = self.session.client("ce", region_name="us-east-1")
        self.ec2 = self.session.client("ec2")

    def get_cost_data(self, start_date: date, end_date: date) -> list[dict]:
        response = self.cost_explorer.get_cost_and_usage(
            TimePeriod={"Start": start_date.isoformat(), "End": end_date.isoformat()},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}, {"Type": "DIMENSION", "Key": "REGION"}],
        )

        rows: list[dict] = []
        for result in response.get("ResultsByTime", []):
            for grp in result.get("Groups", []):
                amount = grp["Metrics"]["UnblendedCost"]["Amount"]
                rows.append(
                    {
                        "date": result["TimePeriod"]["Start"],
                        "service": grp["Keys"][0],
                        "region": grp["Keys"][1],
                        "amount_usd": float(amount),
                        "currency": grp["Metrics"]["UnblendedCost"]["Unit"],
                    }
                )
        return rows

    def list_resources(self) -> list[dict]:
        instances = self.ec2.describe_instances()
        resources: list[dict] = []
        for reservation in instances.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                resources.append({"resource_id": instance["InstanceId"], "type": "ec2"})
        return resources

    def get_utilization_metrics(self, resource_id: str, days: int = 14) -> dict:
        return {"resource_id": resource_id, "days": days, "cpu_avg": None, "source": "cloudwatch_pending"}

    def apply_action(self, action: dict, dry_run: bool = True) -> dict:
        return {"dry_run": dry_run, "action": action, "status": "simulated" if dry_run else "queued"}
