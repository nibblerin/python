from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def execute(self, query: str, params = None) -> None:
        pass

    @abstractmethod
    def executemany(self, query: str, data) -> None:
        pass

    @abstractmethod
    def fetchall(self, query: str, params = None) -> list[dict]:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None:
            self.rollback()
        self.close()
        return False