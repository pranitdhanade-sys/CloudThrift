"""Ports for cloud provider integrations used by the core agent layer."""

from abc import ABC, abstractmethod
from datetime import date


class CloudAdapter(ABC):
    """Abstract cloud adapter interface for all provider implementations."""

    @abstractmethod
    def get_cost_data(self, start_date: date, end_date: date) -> list[dict]:
        """Fetch cost data for a time window."""

    @abstractmethod
    def list_resources(self) -> list[dict]:
        """List relevant resources for optimization analysis."""

    @abstractmethod
    def get_utilization_metrics(self, resource_id: str, days: int = 14) -> dict:
        """Get utilization metrics for a specific resource."""

    @abstractmethod
    def apply_action(self, action: dict, dry_run: bool = True) -> dict:
        """Apply or simulate remediation action."""
