from dataclasses import dataclass

import bcrypt

from .data_handler import QueryDB, WriteDBUser, WriteDBAuction, WriteDBLot
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
class BidOperation:
    user: str

    def create_bid(self, lot_id, amount, time):
        pass
    def get_bids(self, lot_id):
        pass

@dataclass
class LotOperation:
    user: str

    def create_lot(self, auction_id=None, title='', description='', start_price=None, buy_now_price=None, start_time='', end_time=''):
        if auction_id == None:
            raise ValueError("Erro: Sem leilão a relacionar!")
        if title == '':
            raise ValueError("Erro: Título não enviado!")
        if description == '':
            raise ValueError("Erro: Descrição vazia!")
        if start_price == None:
            raise ValueError("Erro: Preço inicial não informado!")
        if buy_now_price == None:
            raise ValueError("Erro: Preço de compra imediata não informado!")
        if start_time == '': 
            raise ValueError("Erro: Início do lote vazio!")
        if end_time == '':
            raise ValueError("Erro: Fim do lote vazio!")
        writer = WriteDBLot(self.user, auction_id, title, description, start_price, buy_now_price, start_time, end_time)
        writer.write()
        return "Lote criado e associado a leilão!"

    def get_lots(self, auction_id):
        pass
    
    def get_lot(self, lot_id):
        pass

    def append_bid(self):
        pass

@dataclass
class AuctionOperation:
    user: str

    def create_auction(self='', title='', description='', start_time='', end_time=''):
        if title == '':
            raise ValueError("Erro: Título não enviado!")
        if description == '':
            raise ValueError("Erro: Descrição vazia!")
        if start_time == '': 
            raise ValueError("Erro: Início do leilão vazio!")
        if end_time == '':
            raise ValueError("Erro: Fim do leilão vazio!")
        auction_writer = WriteDBAuction(username=self.user, title=title, description=description, start_time=start_time, end_time=end_time)
        auction_writer.write()
        return "Leilao registrado com sucesso!"

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
    
    def get_one_auction(self, auction_id):
        if not auction_id:
            raise ValueError("Não foi fornecido leilão para buscar!")
        auction = QueryDB(Auction, id=auction_id).query()[0]
        auction = auction.__dict__
        del auction['_sa_instance_state']
        return auction
    
    def append_lot(self, auction_id, title, description, start_price, buy_now_price, start_time, end_time):
        try:    
            if not auction_id:
                raise ValueError("Não foi fornecido leilão para buscar lotes!")
            lot_writer = LotOperation(self.user)
            message = lot_writer.create_lot(auction_id=auction_id, title=title, description=description, start_price=start_price, buy_now_price=buy_now_price, start_time=start_time, end_time=end_time)
            return message
        except ValueError:
            raise ValueError("Erro em adicionar lote a leilão!")
    # def delete_auction(self):
    # destroyer = WriteDBAuction(self.user, )
    # return "Leilão deletado com sucesso!"