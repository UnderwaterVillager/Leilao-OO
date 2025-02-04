from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from app.models import UserAccount

class QueryDB:
    def __init__(self, table, **filter_params):
        self.engine = create_engine('sqlite:///app.db')
        self.table = table
        self.filter_params = filter_params

    def query(self):
        with Session(self.engine) as session:
            result = session.query(self.table)
            if self.filter_params:
                for attr, value in self.filter_params.items():
                    result = result.filter(getattr(self.table, attr) == value)
        return result.all()

class WriteDBUser:
    def __init__(self, username, password, email):
        self.engine = create_engine('sqlite:///app.db')
        self.table = UserAccount
        self.username = username
        self.password = password
        self.email = email 

    def write(self):
        with Session(self.engine) as session:
            session.add(self.table(username=self.username, password=self.password, email=self.email))
            session.commit()
