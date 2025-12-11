from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select

from src.database.db_client import DBClient
from src.database.structure import OrderBookVolumesHistory, CoinStats, OrderBookVolumesHistoryUsdt
from src.models.order_book_models import OrderBookVolumes, OrderBookUsdt


class OrderBookService:

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    async def save_volumes(self, volumes: OrderBookVolumes) -> bool:
        try:
            async with self.db_client.async_session() as session:
                existing = await self.db_client.get_record_by_field('symbol', volumes.symbol)

                if existing:
                    existing.ask_volume_positive = volumes.volume_asks_upper
                    existing.bid_volume_negative = volumes.volume_bids_lower
                    existing.calculate_percentage = volumes.upper_percent
                    existing.upper_price = volumes.price_upper_level
                    existing.average_price = volumes.mid_price
                    existing.lower_price = volumes.price_lower_level
                    existing.timestamp = int(volumes.timestamp.timestamp())
                else:
                    coin_data = {
                        'symbol': volumes.symbol,
                        'ask_volume_positive': volumes.volume_asks_upper,
                        'bid_volume_negative': volumes.volume_bids_lower,
                        'calculate_percentage': volumes.upper_percent,
                        'upper_price': volumes.price_upper_level,
                        'average_price': volumes.mid_price,
                        'lower_price': volumes.price_lower_level,
                        'timestamp': int(volumes.timestamp.timestamp())
                    }
                    new_record = CoinStats(**coin_data)
                    session.add(new_record)

                history_record = OrderBookVolumesHistory(
                    symbol=volumes.symbol,
                    timestamp=int(volumes.timestamp.timestamp()),
                    volume_asks_upper=volumes.volume_asks_upper,
                    volume_bids_lower=volumes.volume_bids_lower,
                    nonce=volumes.nonce
                )
                session.add(history_record)

                await session.commit()

            return True

        except Exception as e:
            print(f"❌ Error saving volumes: {e}")
            return False

    async def save_volumes_usdt(self, volumes: OrderBookUsdt) -> bool:
        try:
            async with self.db_client.async_session() as session:
                existing = await self.db_client.get_record_by_field('symbol', volumes.symbol)

                if existing:
                    existing.calculate_percentage = volumes.upper_percent
                    existing.average_price = volumes.mid_price
                    existing.timestamp = int(volumes.timestamp.timestamp())
                else:
                    coin_data = {
                        'symbol': volumes.symbol,
                        'calculate_percentage': volumes.upper_percent,
                        'average_price': volumes.mid_price,
                        'timestamp': int(volumes.timestamp.timestamp())
                    }
                    new_record = CoinStats(**coin_data)
                    session.add(new_record)

                history_record = OrderBookVolumesHistoryUsdt(
                    symbol=volumes.symbol,
                    timestamp=int(volumes.timestamp.timestamp()),
                    avarage_ask_volume=volumes.avarage_ask_limit_volume,
                    avarage_bids_volume=volumes.avarage_bid_limit_volume,
                    nonce=volumes.nonce )
                session.add(history_record)

                await session.commit()

            return True

        except Exception as e:
            print(f"❌ Error saving volumes: {e}")
            return False

    async def get_usdt_limits_for_period(
            self,
            symbol: str,
            period_minutes: int
    ) -> List[OrderBookVolumesHistoryUsdt]:

        cutoff_timestamp = int((datetime.now() - timedelta(minutes=period_minutes)).timestamp())

        stmt = (
            select(OrderBookVolumesHistoryUsdt)
            .where(
                OrderBookVolumesHistoryUsdt.symbol == symbol,
                OrderBookVolumesHistoryUsdt.timestamp >= cutoff_timestamp
            )
            .order_by(OrderBookVolumesHistoryUsdt.timestamp.desc())
        )

        async with self.db_client.async_session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_volumes_for_period(
            self,
            symbol: str,
            period_minutes: int
    ) -> List[OrderBookVolumesHistory]:

        cutoff_timestamp = int((datetime.now() - timedelta(minutes=period_minutes)).timestamp())

        stmt = (
            select(OrderBookVolumesHistory)
            .where(
                OrderBookVolumesHistory.symbol == symbol,
                OrderBookVolumesHistory.timestamp >= cutoff_timestamp
            )
            .order_by(OrderBookVolumesHistory.timestamp.desc())
        )

        async with self.db_client.async_session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()