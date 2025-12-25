from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, BigInteger
from src.db.base import Base

class UserConfig(Base):
    __tablename__ = "user_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    threshold_persentage: Mapped[float] = mapped_column(Float, nullable=True)
    deviation_period_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
