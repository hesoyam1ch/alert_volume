from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Float, Integer, String, DateTime


class Base(DeclarativeBase):
    pass


class CoinStats(Base):
    __tablename__ = f"coin_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    ask_volume_positive: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bid_volume_negative: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calculate_percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    upper_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    average_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lower_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    average_volume: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    timestamp: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


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