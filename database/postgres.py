import os
import psycopg
from psycopg.rows import dict_row
from database.interface import Database

class PostgresDatabase(Database):
    def __init__(
        self,
        host: str,
        port: str,
        dbname: str,
        user: str,
        password: str,
    ):
        self._connection = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            row_factory=dict_row,
        )

    @classmethod
    def from_env(cls) -> "PostgresDatabase":
        return cls(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
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

    def __enter__(self) -> "PostgresDatabase":
        return self
    
    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None:
            self.rollback()
        self.close()
        return False