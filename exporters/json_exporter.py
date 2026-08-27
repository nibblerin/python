import json
from pathlib import Path

from exporters.interface import ReportExporter

class JsonExporter(ReportExporter):

    def export(
        self,
        data: dict,
        file_path: str | Path
    ) -> None:
        path = Path(file_path)
        with path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
                default=str
            )