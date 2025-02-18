from abc import ABC, abstractmethod

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session

from app.models import UserAccount, Auction

class QueryDB:
    def __init__(self, main_table, *join_tables, **filter_params):
        self.engine = create_engine('sqlite:///app.db')
        self.table = main_table
        self.join_tables = join_tables
        self.filter_params = filter_params

    def query(self):
        if self.join_tables:
            with Session(self.engine) as session:
                result = session.query(self.table)
                for join_table in self.join_tables:
                    result = result.join(join_table['join_table'], and_(*join_table['conditions']))
                    for attr, value in join_table['filters'].items():
                        result = result.filter(getattr(join_table['join_table'], attr) == value)
                if self.filter_params:
                    for attr, value in self.filter_params.items():
                        result = result.filter(getattr(self.table, attr) == value)
            return result.all()
        else:
            with Session(self.engine) as session:
                result = session.query(self.table)
                if self.filter_params:
                    for attr, value in self.filter_params.items():
                        result = result.filter(getattr(self.table, attr) == value)
            return result.all()

class WriteDB(ABC):
    def __init__(self, username):
        self.engine = create_engine('sqlite:///app.db')
        self.username = username

    @abstractmethod
    def write():
        pass

class WriteDBUser(WriteDB):
    def __init__(self, username, password, email):
        super().__init__(username)
        self.table = UserAccount
        self.password = password
        self.email = email 

    def write(self):
        with Session(self.engine) as session:
            session.add(self.table(username=self.username, password=self.password, email=self.email))
            session.commit()

class WriteDBAuction(WriteDB):
    def __init__(self, username, title, description, start_time, end_time):
        super().__init__(username)
        self.table = Auction
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time

    def write(self):
        with Session(self.engine) as session:
            user_query = session.query(UserAccount).filter_by(username=self.username)[0]
            session.add(self.table(seller=user_query, title=self.title, description=self.description, start_time=self.start_time, end_time=self.end_time))
            session.commit()
                