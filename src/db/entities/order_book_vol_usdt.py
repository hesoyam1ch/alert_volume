from sqlalchemy import Integer, String, Float, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class OrderBookVolumesHistoryUsdt(Base):
    __tablename__ = "order_book_volumes_history_usdt"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False, index=True)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    avarage_bids_volume: Mapped[float] = mapped_column(Float, nullable=False)
    avarage_ask_volume: Mapped[float] = mapped_column(Float, nullable=False)
    nonce: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
