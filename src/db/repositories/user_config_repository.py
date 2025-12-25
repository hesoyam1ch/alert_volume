from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.entities.user_config  import UserConfig
from src.db.repositories.base_repository import BaseRepository

class UserConfigRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(UserConfig, session)

    async def create_config(self, user_id: int, symbol: str, threshold_percentage: float = None, deviation_period_minutes: int = None):
        result = await self.session.execute(select(UserConfig).where(UserConfig.user_id == user_id))
        config = result.scalars().first()

        if config:
            config.symbol = symbol
            config.threshold_persentage = threshold_percentage #need to rename
            config.deviation_period_minutes = deviation_period_minutes
        else:
            config = UserConfig(
                user_id=user_id,
                symbol=symbol,
                threshold_persentage=threshold_percentage, # need to rename
                deviation_period_minutes=deviation_period_minutes
            )
            self.session.add(config)

        await self.session.commit()
        await self.session.refresh(config)

    async def get_by_user_id(self, user_id: int)->UserConfig:
        result = await self.session.execute(
            select(UserConfig).where(
                UserConfig.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()
