from pathlib import Path

from dotenv import load_dotenv

from cli.parser import parse_arguments
from database.postgres import PostgresDatabase
from exporters.factory import create_exporter
from reader.json_reader import JsonFileReader
from services.import_srv import ImportService
from services.report_srv import ReportService
from services.schema_srv import SchemaService

def main() -> None:
    load_dotenv()
    args = parse_arguments()

    with PostgresDatabase.from_env() as db:

        if not args.export_only:
            schema = SchemaService(db)

            schema.drop_tables()
            schema.apply_file("sql/schema.sql")

            if args.use_indexes:
                schema.apply_file("sql/indexes.sql")

            importer = ImportService(db, JsonFileReader())
            importer.load_rooms(args.rooms)
            importer.load_students(args.students)

            db.commit()

        data = ReportService(db).build_all_reports()

        create_exporter(args.format).export(data)


if __name__ == "__main__":
    main()