from abc import ABC, abstractmethod
from pathlib import Path


class ReportExporter(ABC):
    @abstractmethod
    def export(self, data: dict, file_path: str | Path) -> None:
        ...