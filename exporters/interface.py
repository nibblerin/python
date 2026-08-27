from abc import ABC, abstractmethod

class ReportExporter(ABC):
    @abstractmethod
    def export(self, data: dict, file_path: str) -> None:
        ...