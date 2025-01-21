from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text

class Base(DeclarativeBase):
    pass

class Documents(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    user_id: Mapped[int] = mapped_column(Column(Integer, ForeignKey('users.id')))
    auction_id: Mapped[int] = mapped_column(Column(Integer, ForeignKey('auctions.id')))
    lot_id: Mapped[int] = mapped_column(Column(Integer, ForeignKey('lots.id')))
    path: Mapped[str] = mapped_column(Column(String))


class Bids(Base):
    __tablename__ = 'bids'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    lot_id: Mapped[int] = mapped_column(Column(Integer, ForeignKey('lots.id')))
    bidder: Mapped[int] = mapped_column(Column(Integer, ForeignKey('users.id')))
    amount: Mapped[float] = mapped_column(Column(Float))
    time: Mapped[str] = mapped_column(Column(DateTime))

class Notifications(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    user_id: Mapped[int] = mapped_column(Column(Integer, ForeignKey('users.id')))
    message: Mapped[str] = mapped_column(Column(Text))
    time: Mapped[str] = mapped_column(Column(DateTime))

class SoldItems(Base):
    __tablename__ = 'sold_items'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    lot_id: Mapped[int] = mapped_column(Column(Integer, ForeignKey('lots.id')))
    buyer: Mapped[int] = mapped_column(Column(Integer, ForeignKey('users.id')))
    time: Mapped[str] = mapped_column(Column(DateTime))

class UserAccount(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    username: Mapped[str] = mapped_column(Column(String))
    password: Mapped[str] = mapped_column(Column(String))
    email: Mapped[str] = mapped_column(Column(String))

class Auction(Base):
    __tablename__ = 'auctions'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    title: Mapped[str] = mapped_column(Column(String))
    description: Mapped[str] = mapped_column(Column(Text))
    start_time: Mapped[str] = mapped_column(Column(DateTime))
    end_time: Mapped[str] = mapped_column(Column(DateTime))
    seller: Mapped[int] = mapped_column(Column(Integer, ForeignKey('users.id')))
    notifications: Mapped[int] = mapped_column(Column(Integer, ForeignKey('notifications.id')))



class Lot(Base):
    __tablename__ = 'lots'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    auction_id: Mapped[int] = mapped_column(Column(Integer, ForeignKey('auctions.id')))
    title: Mapped[str] = mapped_column(Column(String))
    description: Mapped[str] = mapped_column(Column(Text))
    start_price: Mapped[float] = mapped_column(Column(Float))
    buy_now_price: Mapped[float] = mapped_column(Column(Float))
    start_time: Mapped[str] = mapped_column(Column(DateTime))
    end_time: Mapped[str] = mapped_column(Column(DateTime))
    seller: Mapped[int] = mapped_column(Column(Integer, ForeignKey('users.id')))
    image_path: Mapped[str] = mapped_column(Column(String))