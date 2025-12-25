from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped
from src.db.base import Base


class OrderBookVolumesHistory(Base):
    __tablename__ = "orderbook_volumes_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False, index=True)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    volume_asks_upper: Mapped[float] = mapped_column(Float, nullable=False)
    volume_bids_lower: Mapped[float] = mapped_column(Float, nullable=False)
    nonce: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)