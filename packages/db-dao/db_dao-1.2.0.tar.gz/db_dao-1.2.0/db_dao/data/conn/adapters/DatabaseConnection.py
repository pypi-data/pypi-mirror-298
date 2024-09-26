import abc
from data.conn.adapters.DatabaseCursor import DatabaseCursor

class DatabaseConnection(abc.ABC):
    @abc.abstractmethod
    def cursor(self) -> DatabaseCursor:
        pass

    @abc.abstractmethod
    def commit(self) -> None:
        pass

    @abc.abstractmethod
    def rollback(self) -> None:
        pass