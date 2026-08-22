from database.base import Database
from services.import_srv import ImportService
from services.report_srv import ReportService
from services.export_srv import ExportService


def main():
    db = Database()

    try:
        importer = ImportService(db)
        reports = ReportService(db)
        exporter = ExportService()

        importer.load_rooms("data/rooms.json")
        importer.load_students("data/students.json")

        results = reports.build_all_reports()

        exporter.to_json(
            results,
            "results.json"
        )

        db.rollback()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()