from sqlalchemy import Column, Integer, BigInteger, String

from .base import Base
from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<User(id={self.id}, user_id={self.user_id}, username={self.username})>"
        )


