from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.entities.order_book_vol import OrderBookVolumesHistory
from src.db.entities.order_book_vol_usdt import  OrderBookVolumesHistoryUsdt
from src.db.repositories.base_repository import BaseRepository

class OrderBookVolumesHistoryRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(OrderBookVolumesHistory, session)

    async def get_latest_by_symbol(self, symbol: str):
        result = await self.session.execute(
            select(OrderBookVolumesHistory)
            .where(OrderBookVolumesHistory.symbol == symbol)
            .order_by(OrderBookVolumesHistory.timestamp.desc())
        )
        return result.scalars().first()

class OrderBookVolumesHistoryUsdtRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(OrderBookVolumesHistoryUsdt, session)

    async def get_latest_by_symbol(self, symbol: str):
        result = await self.session.execute(
            select(OrderBookVolumesHistoryUsdt)
            .where(OrderBookVolumesHistoryUsdt.symbol == symbol)
            .order_by(OrderBookVolumesHistoryUsdt.timestamp.desc())
        )
        return result.scalars().first()

    async def get_for_period(self, symbol: str, cutoff_timestamp: int):
        stmt = (
            select(self.model)
            .where(self.model.symbol == symbol, self.model.timestamp >= cutoff_timestamp)
            .order_by(self.model.timestamp.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()