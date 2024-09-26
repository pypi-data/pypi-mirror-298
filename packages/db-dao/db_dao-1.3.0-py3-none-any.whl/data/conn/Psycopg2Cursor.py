from typing import List, Tuple
from psycopg2.extensions import cursor as Psycopg2CursorType
from psycopg2.extras import execute_batch
from data.conn.DatabaseCursor import DatabaseCursor

class Psycopg2Cursor(DatabaseCursor):
    def __init__(self, cursor: Psycopg2CursorType) -> None:
        self.cursor = cursor

    def execute(self, query: str, params: Tuple = ()) -> None:
        self.cursor.execute(query, params)

    def fetchall(self) -> List[Tuple]:
        return self.cursor.fetchall()

    def fetchone(self) -> Tuple:
        return self.cursor.fetchone()
    
    def execute_batch(self, query: str, lst_data: List[dict]):
        execute_batch(self.cursor, query, lst_data, page_size=100)

    def close(self) -> None:
        self.cursor.close()