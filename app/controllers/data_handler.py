from sqlalchemy import create_engine, select 
from sqlalchemy.orm import Session

class DBOperation:
    def __init__(self):
        self.engine = create_engine('sqlite:///app.db')

class QueryDB(DBOperation):
    def __init__(self, table, **filter_params):
        super().__init__()
        self.table = table
        self.filter_params = filter_params

    def query(self):
        if self.filter_params:
            with Session(self.engine) as session:
                query = select(self.table).filter_by(self.filter_params)
                result = session.execute(query)
        else:
            with Session(self.engine) as session:
                query = select(self.table)
                result = session.execute(query)
        return result

class WriteDB(DBOperation):
    def __init__(self, table, **data):
        super().__init__()
        self.table = table
        self.data = data

    def write(self, data):
        with Session(self.engine) as session:
            session.add(self.table(**data))
            session.commit()
