from data.DAO.GenericDAO import GenericDAO
from data.conn.adapters.DatabaseConnection import DatabaseConnection

class GenericDAOImp(GenericDAO):
    def __init__(self, table: str, conn: DatabaseConnection) -> None:
        self.conn = conn
        self.table = table

    def find_by_id(self, id: str | int):
        query = f'SELECT * FROM {self.table} WHERE {self.table}.id = %s'
        try:
            cur = self.conn.cursor()
            cur.execute(query, (id,))
            data = cur.fetchall()

            return data
        except Exception as e:
            raise e
        

    def find_by_data(self, data: dict):
        field = str(list(data.keys())[0])
        query = f'SELECT * FROM {self.table} WHERE {self.table}.{field} = %s'
        value = data[field]
        try:
            cur = self.conn.cursor()
            cur.execute(query, (value,))
            data = cur.fetchall()

            return data
        except Exception as e:
            raise e

    def find_by_cond(self, cond: str):
        query = f'''SELECT * FROM {self.table} WHERE {cond}'''
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            data = cur.fetchall()

            return data
        except Exception as e:
            raise e
        

    def create(self, data: dict) -> str:

        fields = ', '.join(data.keys())
        sql_values = ', '.join('%s' for _ in data.values())
        query = f"INSERT INTO {self.table} ({fields}) VALUES ({sql_values}) RETURNING id"
    
        values = tuple(data.values())
        try:
            cur = self.conn.cursor()
            cur.execute(query, values)
            self.conn.commit()
            return cur.fetchone()[0]
        except Exception as e:
            self.conn.rollback()
            raise e
        
    def create_with_batch(self, lst_data: list[dict], on_conflict: list[str] = []) -> str:
        if not lst_data:
            return
        
        columns = list(lst_data[0].keys())
        
        placeholders = ', '.join(['${}'.format(i+1) for i in range(len(columns))])
        column_names = ', '.join(columns)
        conflict_column = ', '.join(on_conflict)
        if len(on_conflict) > 0:
            query = 'PREPARE insertStmt AS INSERT INTO {} ({}) VALUES ({}) ON CONFLICT ({}) DO NOTHING'.format(self.table, column_names, placeholders, conflict_column)
        else:
            query = 'PREPARE insertStmt AS INSERT INTO {} ({}) VALUES ({})'.format(self.table, column_names, placeholders)

        cur = self.conn.cursor()
        cur.execute(query)
        cur.execute_batch("EXECUTE insertStmt ({})".format(', '.join('%({})s'.format(col) for col in columns)), lst_data)
        
        cur.execute("DEALLOCATE insertStmt")
        self.conn.commit()
        cur.close()
        
    def update(self, primary_key_value, data: dict, primary_key_name='id'):
        set_fields = ', '.join([f"{key} = %s" for key in data.keys()])
        
        query = f"UPDATE {self.table} SET {set_fields} WHERE {primary_key_name} = %s"
        
        values = list(data.values())
        values.append(primary_key_value)

        try:
            cur = self.conn.cursor()
            cur.execute(query, tuple(values))
            self.conn.commit()
            # return cur.rowcount
        except Exception as e:
            self.conn.rollback()
            raise e
        
    
    def delete(self, where_field: str ,id: str):
        query = f"""DELETE FROM {self.table} WHERE {where_field} = '{id}'"""
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e