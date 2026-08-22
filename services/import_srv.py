import json
from datetime import datetime
from database.base import Database

class ImportService:
    def __init__(self, db: Database):
        self._db = db

    def load_rooms(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as file:
            rooms = json.load(file)

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
        with open(file_path, "r", encoding="utf-8") as file:
            students = json.load(file)

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
