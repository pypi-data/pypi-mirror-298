from abc import ABC, abstractmethod
from typing import Any, Tuple, List

class DatabaseCursor(ABC):
    @abstractmethod
    def execute(self, query: str, params: Tuple = ()) -> None:
        pass

    @abstractmethod
    def fetchall(self) -> List[Tuple]:
        pass

    @abstractmethod
    def fetchone(self) -> Tuple:
        pass

    @abstractmethod
    def execute_batch(query: str, lst_data: list[dict]): pass

    @abstractmethod
    def close(self) -> None: pass