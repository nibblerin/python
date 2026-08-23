from exporters.interface import ReportExporter
from exporters.json_exporter import JsonExporter
from exporters.xml_exporter import XmlExporter

def create_exporter(output_format: str) -> ReportExporter:
    exporters = {
        "json": JsonExporter,
        "xml": XmlExporter,
    }
    try:
        return exporters[output_format]()
    except KeyError:
        raise ValueError(f"Unsupported format: {output_format}")