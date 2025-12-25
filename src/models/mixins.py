from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def formatted_updated_at(self, date_format: str = "%d.%m.%Y %H:%M"):
        if self.updated_at:
            return self.updated_at.strftime(date_format)
        return None

    def formatted_created_at(self, date_format: str = "%d.%m.%Y %H:%M"):
        if self.created_at:
            return self.created_at.strftime(date_format)
        return None
