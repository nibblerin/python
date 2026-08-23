import json
from datetime import datetime
from database.interface import Database
from reader.json_reader import JsonFileReader

class ImportService:
    def __init__(self, db: Database, reader: JsonFileReader):
        self._db = db
        self._reader = reader

    def load_rooms(self, file_path: str) -> None:
        rooms = self._reader.read(file_path)

        query = """
            INSERT INTO rooms (id, name)
            VALUES (%s, %s)
        """

        data = [
            (room["id"], room["name"])
            for room in rooms
        ]

        self._db.executemany(query, data)

    def load_students(self, file_path: str) -> None:
        students = self._reader.read(file_path)

        query = """
            INSERT INTO students
                (birthday, id, name, room_id, sex)
            VALUES (%s, %s, %s, %s, %s)
        """

        data = [
            (
                datetime.fromisoformat(student["birthday"]),
                student["id"],
                student["name"],
                student["room"],
                student["sex"]
            )
            for student in students
        ]

        self._db.executemany(query, data)
