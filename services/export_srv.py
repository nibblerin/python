import json
import xml.etree.ElementTree as ET

class ExportService:

    def to_json(
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

    def to_xml(
        self,
        data: dict,
        file_path: str = "result_xml.xml"
    ) -> None:
        root = ET.Element("reports")

        for report_name, rows in data.items():
            report = ET.SubElement(root, report_name)

            for row in rows:
                item = ET.SubElement(report, "item")

                for key, value in row.items():
                    field = ET.SubElement(item, key)
                    field.text = str(value)

        tree = ET.ElementTree(root)
        tree.write(
            file_path,
            encoding="utf-8",
            xml_declaration=True
        )