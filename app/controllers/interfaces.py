import bcrypt
from sqlalchemy import text

from .data_handler import WriteDBUser, QueryDB
from ..models import UserAccount

class UserDataInterface:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.errors = []
    
    def query_data(self, table, **data):
        query = QueryDB(table, **data)
        result = query.query()
        return result

    def write_data(self, username, password, email):
        writer = WriteDBUser(username, password, email)
        writer.write()
        return 'Dado registrado com sucesso'

    def encrypt_password(self):
        bytes = self.password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        return hash
    
    def check_password(self, hash):
        bytes = self.password.encode('utf-8')
        return bcrypt.checkpw(bytes, hash)

class SignUp(UserDataInterface):
    def __init__(self, username, password, email):
        super().__init__(username, password)
        self.email = email

    def run(self):
        has_username = self.query_data(UserAccount, username=self.username)
        has_email = self.query_data(UserAccount, email=self.email)
        if has_username or has_email:
            if has_username:
                self.errors.append('Nome de usuário já existe')
            if has_email:
                self.errors.append('Email já cadastrado')
            return self.errors
        else:
            print(self.username)
            is_user_created = self.write_data(username=self.username, password=self.encrypt_password(), email=self.email)
            return is_user_created
        

class SignIn(UserDataInterface):
    ...