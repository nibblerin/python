import xml.etree.ElementTree as ET
from exporters.interface import ReportExporter

class XmlExporter(ReportExporter):
    def export(
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
                    field.text = "" if value is None else str(value)

        tree = ET.ElementTree(root)

        ET.indent(tree, space="    ")

        tree.write(
            file_path,
            encoding="utf-8",
            xml_declaration=True
        )