import json

from exporters.interface import ReportExporter

class JsonExporter(ReportExporter):

    def export(
        self,
        data: dict,
        file_path: str = "result_json.json"
    ) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
                default=str
            )