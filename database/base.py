import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
load_dotenv()

class Database:
    def __init__(self):
        self._connection = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            row_factory=dict_row,
        )

    def execute(self, query: str, params=None) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(query, params)

    def executemany(self, query: str, data) -> None:
        with self._connection.cursor() as cursor:
            cursor.executemany(query, data)

    def commit(self) -> None:
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def fetchall(self, query, params=None):
        with self._connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    def rollback(self) -> None:
        self._connection.rollback()