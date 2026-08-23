from pathlib import Path
from database.interface import Database

class SchemaService:
    def __init__(self, db: Database) -> None:
        self._db = db

    def apply_file(self, file_path: str | Path) -> None:
        sql = Path(file_path).read_text(encoding="utf-8")
        for statement in sql.split(";"):
            statement = statement.strip()
            if statement:
                self._db.execute(statement)

    def drop_tables(self) -> None:
        self._db.execute(
            "DROP TABLE IF EXISTS students, rooms CASCADE"
        )