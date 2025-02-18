from dataclasses import dataclass

import bcrypt
from sqlalchemy import text

from .data_handler import QueryDB, WriteDBUser, WriteDBAuction
from ..models import UserAccount, Auction

class UserDataInterface:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def query_data(self, table, **data):
        query = QueryDB(table, **data)
        result = query.query()
        return result

    def write_data(self, username, password, email):
        writer = WriteDBUser(username, password, email)
        writer.write()
        return 'Usuário registrado com sucesso'

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
                raise ValueError('Erro: Nome de usuário já existe')
            if has_email:
                raise ValueError('Erro: Email já cadastrado')
        else:
            is_user_created = self.write_data(username=self.username, password=self.encrypt_password(), email=self.email)
            return is_user_created
        

class SignIn(UserDataInterface):
    def __init__(self, username, password):
        super().__init__(username, password)

    def run(self):
        user = self.query_data(UserAccount, username=self.username)
        if user:
            if self.check_password(user[0].password):
                return "Usuário está autenticado!"
            else:
                raise ValueError("Erro: Senha incorreta!")
        else:
            raise ValueError("Erro: Usuário não encontrado!")




@dataclass
class AuctionOperation:
    user: str
    _auction_id : int = None
    _title: str = ''
    _description: str = ''
    _start_time: str = ''
    _end_time: str = '' 

    @property
    def auction_id(self):
        return self._auction_id
    @property
    def title(self):
        return self._title
    @property
    def description(self):
        return self._description
    @property
    def start_time(self):
        return self._start_time
    @property
    def end_time(self):
        return self._end_time
    
    @auction_id.setter
    def auction_id(self, value):
        self._auction_id = value

    @title.setter
    def title(self, value):
        self._title = value

    @description.setter
    def description(self, value):
        self._description = value

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

class AuctionWrite(AuctionOperation):
    def create_auction(self, title, description, start_time, end_time):
        if title == '':
            raise ValueError("Erro: Título não enviado")
        if description == '':
            raise ValueError("Erro: Descrição vazia!")
        if start_time == '': 
            raise ValueError("Erro: Início do leilão vazio!")
        if end_time == '':
            raise ValueError("Erro: Fim do leilão vazio!")
        auction_writer = WriteDBAuction(username=self.user, title=title, description=description, start_time=start_time, end_time=end_time)
        auction_writer.write()
        return "Leilao registrado com sucesso"

    
class AuctionGet(AuctionOperation):
    def get_auctions(self, by_owner=False):
        auctions_data = []
        if by_owner == False:
            auctions = QueryDB(Auction).query()
        else:
            auctions = QueryDB((Auction), {'join_table': UserAccount, 'filters': {"username":
            self.user}, 'conditions': [Auction.seller_id == UserAccount.id]}).query()
        for data in auctions:
            data = data.__dict__
            del data['_sa_instance_state']
            auctions_data.append(data)
        return auctions_data
        