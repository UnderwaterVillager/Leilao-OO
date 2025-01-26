from typing import List, Optional

from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text

class Base(DeclarativeBase):
    pass

class Documents(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    path: Mapped[str] = mapped_column(Column(String))

    user_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('users.id')))
    user: Mapped["UserAccount" | None] = relationship(back_populates="documents") 
    auction_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('auctions.id')))
    auction: Mapped["Auction" | None] = relationship(back_populates="documents")
    lot_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('lots.id')))
    lot: Mapped["Lot" | None] = relationship(back_populates="documents")


class Bids(Base):
    __tablename__ = 'bids'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    amount: Mapped[float] = mapped_column(Column(Float))
    time: Mapped[str] = mapped_column(Column(DateTime))

    lot_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('lots.id')))
    lot: Mapped["Lot" | None] = relationship(back_populates="bids")
    bidder_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('users.id')))
    bidder: Mapped["UserAccount" | None] = relationship(back_populates="bids")

class Notifications(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    message: Mapped[str] = mapped_column(Column(Text))
    time: Mapped[str] = mapped_column(Column(DateTime))

    user_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('users.id')))
    user: Mapped["UserAccount" | None] = relationship(back_populates="notifications")

class UserAccount(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    username: Mapped[str] = mapped_column(Column(String))
    password: Mapped[str] = mapped_column(Column(String))
    email: Mapped[str] = mapped_column(Column(String))

    auctions: Mapped[List["Auction"]] = relationship(back_populates="seller")
    documents: Mapped[List["Documents"]] = relationship(back_populates="user")
    bids: Mapped[List["Bids"]] = relationship(back_populates="bidder")
    notifications: Mapped[List["Notifications"]] = relationship(back_populates="user")
    bought_items: Mapped[List["Lot"]] = relationship(back_populates="lot")
    sold_items: Mapped[List["Lot"]] = relationship(back_populates="lot")
    logs: Mapped[List["Log"]] = relationship(back_populates="actor")

class Auction(Base):
    __tablename__ = 'auctions'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    title: Mapped[str] = mapped_column(Column(String))
    description: Mapped[str] = mapped_column(Column(Text))
    start_time: Mapped[str] = mapped_column(Column(DateTime))
    end_time: Mapped[str] = mapped_column(Column(DateTime))

    documents: Mapped[List["Documents"]] = relationship(back_populates="auction")
    lots: Mapped[List["Lot"]] = relationship(back_populates="auction")
    seller_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('users.id')))
    seller: Mapped["UserAccount" | None] = relationship(back_populates="auctions")
    logs: Mapped[List["Log"]] = relationship(back_populates="auction")


class Lot(Base):
    __tablename__ = 'lots'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    title: Mapped[str] = mapped_column(Column(String))
    description: Mapped[str] = mapped_column(Column(Text))
    start_price: Mapped[float] = mapped_column(Column(Float))
    buy_now_price: Mapped[float] = mapped_column(Column(Float))
    start_time: Mapped[str] = mapped_column(Column(DateTime))
    end_time: Mapped[str] = mapped_column(Column(DateTime))
    image_path: Mapped[str] = mapped_column(Column(String))

    auction_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('auctions.id')))
    auction: Mapped["Auction" | None] = relationship(back_populates="lots")
    documents: Mapped[List["Documents"]] = relationship(back_populates="lot")
    bids: Mapped[List["Bids"]] = relationship(back_populates="lot")
    seller_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('users.id')))
    seller: Mapped["UserAccount" | None] = relationship(back_populates="")
    buyer_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('users.id')))
    buyer: Mapped["UserAccount" | None] = relationship(back_populates="user.id")
    logs: Mapped[List["Log"]] = relationship(back_populates="lot")

class Log(Base):
    __tablename__ = 'logs'

    id: Mapped[int] = mapped_column(Column(Integer, primary_key=True))
    time: Mapped[str] = mapped_column(Column(DateTime))
    action_id: Mapped[str] = mapped_column(Column(String))

    actor_id: Mapped[int| None] = mapped_column(Column(Integer, ForeignKey('users.id')))
    actor: Mapped["UserAccount" | None] = relationship(back_populates="logs")
    auction_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('auctions.id')))
    auction: Mapped["Auction" | None] = relationship(back_populates="logs")
    lot_id: Mapped[int | None] = mapped_column(Column(Integer, ForeignKey('lots.id')))
    lot: Mapped["Lot" | None] = relationship(back_populates="logs")
    

