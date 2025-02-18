import unittest
import datetime

from app.models import create, destroy
from app.models import UserAccount, Auction
from app.controllers.interfaces import SignUp, AuctionWrite, AuctionGet, QueryDB

class TestWriteAuction(unittest.TestCase):
    def setUp(self):
        destroy()
        create()
        SignUp('Marco', 'Polo', 'shambala@yahoo.com').run()
    
    def test_save_auction(self):
        start_time = datetime.datetime(2025, 3, 15, hour=3)
        end_time = datetime.datetime(2025, 3, 15, hour=3)
        
        writer= AuctionWrite(user='Marco')
        result = writer.create_auction(title='Consoles que morreram antes da hora!', description='Gemas do games que, apesar de partirem cedo, ainda carregam um espaço enorme no coração de jogadores', start_time=start_time, end_time=end_time)

        self.assertEqual(result, "Leilao registrado com sucesso")

    def test_save_auction_no_title(self):
        start_time = datetime.datetime(2025, 3, 15, hour=3)
        end_time = datetime.datetime(2025, 3, 15, hour=3)
        
        with self.assertRaises(ValueError) as context:
            writer= AuctionWrite(user='Marco')
            result = writer.create_auction(title='', description='Gemas do games que, apesar de partirem cedo, ainda carregam um espaço enorme no coração de jogadores', start_time=start_time, end_time=end_time)

        self.assertEqual(str(context.exception), "Erro: Título não enviado")
    
    def test_save_auction_no_description(self):
        start_time = datetime.datetime(2025, 3, 15, hour=3)
        end_time = datetime.datetime(2025, 3, 15, hour=3)
        
        with self.assertRaises(ValueError) as context:
            writer= AuctionWrite(user='Marco')
            writer.create_auction(title='Consoles que morreram antes da hora!', description='', start_time=start_time, end_time=end_time)

        self.assertEqual(str(context.exception), "Erro: Descrição vazia!")
    
    def test_save_auction_no_start_time(self):
        end_time = datetime.datetime(2025, 3, 15, hour=3)
        with self.assertRaises(ValueError) as context:
            writer= AuctionWrite(user='Marco')
            writer.create_auction(title='Consoles que morreram antes da hora!', description='Gemas do games que, apesar de partirem cedo, ainda carregam um espaço enorme no coração de jogadores', start_time='', end_time=end_time)

        self.assertEqual(str(context.exception), "Erro: Início do leilão vazio!")
    
    def test_save_auction_no_end_time(self):
        start_time = datetime.datetime(2025, 3, 15, hour=3)

        with self.assertRaises(ValueError) as context:
            writer= AuctionWrite(user='Marco')
            writer.create_auction(title='Consoles que morreram antes da hora!', description='Gemas do games que, apesar de partirem cedo, ainda carregam um espaço enorme no coração de jogadores', start_time=start_time, end_time='')

        self.assertEqual(str(context.exception), "Erro: Fim do leilão vazio!")

class TestGetAuction(unittest.TestCase):
    def setUp(self):
        destroy()
        create()
        
        SignUp('Marco', 'Polo', 'shambala@yahoo.com').run()
        SignUp('João', 'Boxe', 'cinza@gmail.com').run()
        
        start_time = datetime.datetime(2025, 3, 15, hour=3)
        end_time = datetime.datetime(2025, 3, 15, hour=3)
        
        writer1 = AuctionWrite(user='Marco')
        writer1.create_auction(title='Consoles que morreram antes da hora!', description='Gemas do games que, apesar de partirem cedo, ainda carregam um espaço enorme no coração de jogadores', start_time=start_time, end_time=end_time)
        writer1.create_auction(title="Vasos de porcelana", description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec et nisi et neque iaculis sodales et sit amet ex. Vestibulum tincidunt imperdiet nunc at auctor.", start_time=start_time, end_time=end_time)
        writer2 = AuctionWrite(user='João')
        writer2.create_auction(title="Instrumentos músicas de iniciante!", description="Desde instrumentos de cordas, percursão e teclas, com funcionalidades básicas e custo-benéficas!", start_time=start_time, end_time=end_time)

    def test_get_auction_all_users(self):
        auction_one = QueryDB(Auction, id=1).query()[0].__dict__
        auction_two = QueryDB(Auction, id=2).query()[0].__dict__
        auction_three = QueryDB(Auction, id=3).query()[0].__dict__
        del auction_one['_sa_instance_state']
        del auction_two['_sa_instance_state']
        del auction_three['_sa_instance_state']
        
        getter = AuctionGet(user='Marco')
        auctions = getter.get_auctions()
        auctions_dict = [auction for auction in auctions]
        self.assertListEqual([auction_one, auction_two, auction_three], auctions_dict)

    def test_get_my_auctions(self):
        self.maxDiff = None

        auction_one = QueryDB(Auction, id=1).query()[0].__dict__
        auction_two = QueryDB(Auction, id=2).query()[0].__dict__
        del auction_one['_sa_instance_state']
        del auction_two['_sa_instance_state']

        getter = AuctionGet(user='Marco')
        auctions = getter.get_auctions(by_owner=True)
        auctions_dict_list = [auction for auction in auctions]
        self.assertListEqual([auction_one, auction_two], auctions_dict_list)
