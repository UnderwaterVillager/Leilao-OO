import unittest
from datetime import datetime

from app.models import destroy, create
from app.controllers.interfaces import SignUp, LotOperation, AuctionOperation

class TestCreateLot(unittest.TestCase):
    def setUp(self):
        destroy()
        create()
        
        SignUp('Marco', 'Polo', 'shambala@yahoo.com').run()

        start_time = datetime(2025, 3, 15, hour=15)
        end_time = datetime(2025, 3, 30, hour=21)
        
        writer1 = AuctionOperation(user='Marco')
        writer1.create_auction(title='Consoles que morreram antes da hora!', description='Gemas do games que, apesar de partirem cedo, ainda carregam um espaço enorme no coração de jogadores', start_time=start_time, end_time=end_time)

    def test_create_lot(self):
        start_time = datetime(2025, 3, 15, hour=15)
        end_time = datetime(2025, 3, 15, hour=21)
        operator = LotOperation('Marco')
        result = operator.create_lot(auction_id=1, title="Dreamcast Japonês", description="Lacrado, muito bem conservado, acompanhado de SOnic Adventure", start_price=200.00, buy_now_price=350.00, start_time=start_time, end_time=end_time)

        self.assertEqual(result, "Lote criado e associado a leilão!")