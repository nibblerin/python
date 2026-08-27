from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def execute(self, query: str, params = None) -> None:
        ...

    @abstractmethod
    def executemany(self, query: str, data) -> None:
        ...

    @abstractmethod
    def fetchall(self, query: str, params = None) -> list[dict]:
        ...

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None:
            self.rollback()
        self.close()
        return False