from asyncio import CancelledError
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Iterator, Optional

from sqlalchemy import create_engine, update
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import Session, sessionmaker
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed, wait_random_exponential

from const import SYNC_DB_URL, ASYNC_DB_URL
from src.database.structure import CoinStats, Base

locked_retry = retry(
    retry=retry_if_exception_type((OperationalError, CancelledError)),
    stop=stop_after_attempt(4),
    wait=wait_fixed(1) + wait_random_exponential(multiplier=2, max=60),
)


class DBClient:
    def __init__(self):
        self.sync_engine = create_engine(SYNC_DB_URL)
        self.sync_session_factory = sessionmaker(bind=self.sync_engine, expire_on_commit=False)

        self.async_engine = create_async_engine(ASYNC_DB_URL, connect_args={"timeout": 180})
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine, expire_on_commit=False, class_=AsyncSession
        )

    @asynccontextmanager
    async def async_session(self) -> AsyncIterator[AsyncSession]:
        session = self.async_session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @contextmanager
    def sync_session(cls) -> Iterator[Session]:
        session = cls.sync_session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @locked_retry
    async def add_record(self, **fields):
        record = CoinStats(**fields)
        async with self.async_session() as session:
            session.add(record)
        return record

    @locked_retry
    async def update_record(self, record_id: int, **fields):
        async with self.async_session() as session:
            await session.execute(
                update(CoinStats)
                .where(CoinStats.id == record_id)
                .values(**fields)
            )

    @locked_retry
    async def get_record_by_field(self, field: str, value) -> Optional[CoinStats]:
        stmt = select(CoinStats).where(getattr(CoinStats, field) == value)
        async with self.async_session() as session:
            result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    def create_db(cls):
        engine = create_engine(SYNC_DB_URL)
        Base.metadata.create_all(engine)

    @classmethod
    def get_all_records(cls) -> list[CoinStats]:
        with cls.sync_session() as session:
            return session.query(CoinStats).all()
