from sqlalchemy import create_engine

class QueryDB:
    def __init__(self):
        self.db = DB()

    def get_data(self, query):
        return self.db.query(query)