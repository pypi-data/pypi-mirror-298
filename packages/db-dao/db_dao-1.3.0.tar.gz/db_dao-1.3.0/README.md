## Functions

A PostgresSQL DAO library with SOLID principles.

Make anything data control with this library, like a create with batch, create only one and more.


### GenericDAOImp signature
```python
def find_by_id(self, id: str | int): pass

def find_by_cond(self, cond: str): pass

def find_by_data(self, data: dict): pass

def create(self, data: dict) -> str: pass

def create_with_batch(self, lst_data: list[dict]) -> str: pass

def update(self, primary_key_value, data: dict, primary_key_name='id'): pass

def delete(self, id: str): pass
```

## Initialize
```python
from db_dao.conn import Psycopg2Connection
from db_dao.DAO import GenericDAOImp

conn = Psycopg2Connection({
    'host': 'your-host',
    'database': 'your-db',
    'user': 'your-user',
    'password': 'your-password',
    'port': 'your-port',
    'options': 'your-options',
})

any_dao_imp = GenericDAOImp('table_name', conn)

```

## Dependencies
```sh
pip install psycopg2-binary
```