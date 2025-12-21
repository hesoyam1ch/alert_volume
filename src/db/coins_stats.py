from typing import Optional

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


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