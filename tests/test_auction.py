import unittest
import datetime

from app.models import create, destroy
from app.controllers.interfaces import SignUp, AuctionWrite, AuctionGet

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
        writer2 = AuctionWrite(user='João')
        writer2.create_auction(title="Instrumentos músicas de iniciante!", description="Desde instrumentos de cordas, percursão e teclas, com funcionalidades básicas e custo-benéficas!", start_time=start_time, end_time=end_time)

    def test_get_auction_all_users(self):
        getter = AuctionGet('Marco')
        auctions = getter.get_auctions()
        self.assertIsInstance(auctions, list)

    def test_get_auction_one_user(self):
        ...
    