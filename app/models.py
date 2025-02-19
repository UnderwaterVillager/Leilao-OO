from typing import List, Optional

from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship, declarative_base
from sqlalchemy import String, ForeignKey, DateTime, Float, Text, create_engine

class Base(DeclarativeBase):
    pass

class Lot(Base):
    __tablename__ = 'lots'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    start_price: Mapped[float] = mapped_column(Float)
    buy_now_price: Mapped[float] = mapped_column(Float)
    start_time: Mapped[str] = mapped_column(DateTime)
    end_time: Mapped[str] = mapped_column(DateTime)
    image_path: Mapped[Optional[str]] = mapped_column(String)

    auction_id: Mapped[Optional[int]] = mapped_column(ForeignKey('auctions.id'))
    auction: Mapped[Optional["Auction"]] = relationship("Auction", back_populates="lots")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="lot")
    bids: Mapped[List["Bid"]] = relationship("Bid", back_populates="lot")
    logs: Mapped[List["Log"]] = relationship("Log", back_populates="lot")

    buyer_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)
    buyer: Mapped[Optional["UserAccount"]] = relationship("UserAccount", back_populates="bought_lots", foreign_keys=[buyer_id])


class UserAccount(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

    auctions: Mapped[List["Auction"]] = relationship("Auction", back_populates="seller")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="user")
    bids: Mapped[List["Bid"]] = relationship("Bid", back_populates="bidder")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user")
    logs: Mapped[List["Log"]] = relationship("Log", back_populates="actor")
    bought_lots: Mapped[List["Lot"]] = relationship("Lot", back_populates="buyer", foreign_keys=[Lot.buyer_id])


class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    user: Mapped[Optional["UserAccount"]] = relationship("UserAccount", back_populates="documents") 
    auction_id: Mapped[Optional[int]] = mapped_column(ForeignKey('auctions.id'))
    auction: Mapped[Optional["Auction"]] = relationship("Auction", back_populates="documents")
    lot_id: Mapped[Optional[int]] = mapped_column(ForeignKey('lots.id'))
    lot: Mapped[Optional["Lot"]] = relationship("Lot", back_populates="documents")


class Bid(Base):
    __tablename__ = 'bids'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float)
    time: Mapped[str] = mapped_column(DateTime)

    lot_id: Mapped[Optional[int]] = mapped_column(ForeignKey('lots.id'))
    lot: Mapped[Optional["Lot"]] = relationship("Lot", back_populates="bids")
    bidder_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    bidder: Mapped[Optional["UserAccount"]] = relationship("UserAccount", back_populates="bids")

class Notification(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text)
    time: Mapped[str] = mapped_column(DateTime)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    user: Mapped[Optional["UserAccount"]] = relationship("UserAccount", back_populates="notifications")

class Auction(Base):
    __tablename__ = 'auctions'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    start_time: Mapped[str] = mapped_column(DateTime)
    end_time: Mapped[str] = mapped_column(DateTime)

    documents: Mapped[List["Document"]] = relationship("Document", back_populates="auction")
    lots: Mapped[List["Lot"]] = relationship("Lot", back_populates="auction")
    seller_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    seller: Mapped[Optional["UserAccount"]] = relationship("UserAccount", back_populates="auctions")
    logs: Mapped[List["Log"]] = relationship("Log", back_populates="auction")


class Log(Base):
    __tablename__ = 'logs'

    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[str] = mapped_column(DateTime)
    action_id: Mapped[str] = mapped_column(String)

    actor_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    actor: Mapped[Optional["UserAccount"]] = relationship("UserAccount",back_populates="logs")
    auction_id: Mapped[Optional[int]] = mapped_column(ForeignKey('auctions.id'))
    auction: Mapped[Optional["Auction"]] = relationship("Auction", back_populates="logs")
    lot_id: Mapped[Optional[int]] = mapped_column(ForeignKey('lots.id'))
    lot: Mapped[Optional["Lot"]] = relationship("Lot", back_populates="logs")

def create():
    Base.metadata.create_all(create_engine('sqlite:///app.db'))

def destroy():
    Base.metadata.drop_all(create_engine('sqlite:///app.db'))