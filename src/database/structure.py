from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Float, Integer, String, DateTime

#
# class Base(DeclarativeBase):
#     pass
#
#



class OrderBookVolumesHistoryUsdt(Base):
    __tablename__ = "order_book_volumes_history_usdt"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False, index=True)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    avarage_bids_volume: Mapped[float] = mapped_column(Float, nullable=False)
    avarage_ask_volume: Mapped[float] = mapped_column(Float, nullable=False)
    nonce: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

class OrderBookVolumesHistory(Base):
    __tablename__ = "orderbook_volumes_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False, index=True)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    volume_asks_upper: Mapped[float] = mapped_column(Float, nullable=False)
    volume_bids_lower: Mapped[float] = mapped_column(Float, nullable=False)
    nonce: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)