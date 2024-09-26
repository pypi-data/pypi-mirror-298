import psycopg2

from data.conn.Psycopg2Cursor import Psycopg2Cursor
from data.conn.DatabaseConnection import DatabaseConnection
from data.conn.DatabaseCursor import DatabaseCursor

class Psycopg2Connection(DatabaseConnection):
    def __init__(self, credentials: dict) -> None:


        if 'options' in credentials.keys():
            con = psycopg2.connect(host=credentials['host'], 
            database=credentials['database'],
            user=credentials['user'],
            password=credentials['password'],
            port=credentials['port'],
            options=credentials['options'])
        else:
            con = psycopg2.connect(host=credentials['host'], 
            database=credentials['database'],
            user=credentials['user'],
            password=credentials['password'],
            port=credentials['port'])

        self.conn = con

    def cursor(self) -> DatabaseCursor:
        return Psycopg2Cursor(self.conn.cursor())

    def commit(self) -> None:
        self.conn.commit()

    def rollback(self) -> None:
        self.conn.rollback()
