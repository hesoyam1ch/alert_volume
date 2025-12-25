from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.entities.user import User
from src.db.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def register_user(self,user_id: int, username: str):
        result = await self.session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(user_id=user_id, username=username)
            self.session.add(user)
            await self.session.commit()
        return user

    async def get_by_user_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()
