"""Detector interfaces and registry for pluggable waste detection engine."""

from abc import ABC, abstractmethod

from app.schemas.cost import WasteFindingOut


class WasteDetector(ABC):
    name: str

    @abstractmethod
    def detect(self, resources: list[dict], metrics: dict[str, dict]) -> list[WasteFindingOut]:
        """Detect potential waste findings."""


class DetectorRegistry:
    """Simple in-memory registry for detector plugins."""

    def __init__(self) -> None:
        self._detectors: dict[str, WasteDetector] = {}

    def register(self, detector: WasteDetector) -> None:
        self._detectors[detector.name] = detector

    def all(self) -> list[WasteDetector]:
        return list(self._detectors.values())
