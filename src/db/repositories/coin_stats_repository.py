from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.entities.coins_stats import CoinStats
from src.db.repositories.base_repository import BaseRepository

class CoinStatsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(CoinStats, session)

    async def get_by_symbol(self, symbol: str):
        result = await self.session.execute(
            select(CoinStats).where(CoinStats.symbol == symbol)
        )
        return result.scalar_one_or_none()
