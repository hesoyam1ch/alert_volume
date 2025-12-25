from datetime import datetime, timedelta
from typing import List

from src.db.entities.coins_stats import CoinStats
from src.db.entities.order_book_vol import OrderBookVolumesHistory
from src.db.entities.order_book_vol_usdt import OrderBookVolumesHistoryUsdt
from src.models.order_book_models import OrderBookVolumes, OrderBookUsdt


class OrderBookService:

    def __init__(self, usdt_repo: "OrderBookVolumesHistoryUsdtRepository",coin_repo: "CoinStatsRepository"):
        self.usdt_repo = usdt_repo
        self.coin_repo = coin_repo

    async def save_volumes(self, volumes: OrderBookVolumes) -> bool:
        try:
            existing = await self.usdt_repo.get_latest_by_symbol('symbol', volumes.symbol)

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
                self.coin_repo.add(new_record)

                history_record = OrderBookVolumesHistory(
                    symbol=volumes.symbol,
                    timestamp=int(volumes.timestamp.timestamp()),
                    volume_asks_upper=volumes.volume_asks_upper,
                    volume_bids_lower=volumes.volume_bids_lower,
                    nonce=volumes.nonce
                )
                self.usdt_repo.add(history_record)

            return True

        except Exception as e:
            print(f"❌ Error saving volumes: {e}")
            return False

    async def save_volumes_usdt(self, volumes: OrderBookUsdt) -> bool:
        try:
            existing = await self.usdt_repo.get_latest_by_symbol(volumes.symbol)

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
                await self.coin_repo.add(new_record)

            history_record = OrderBookVolumesHistoryUsdt(
                symbol=volumes.symbol,
                timestamp=int(volumes.timestamp.timestamp()),
                avarage_ask_volume=volumes.avarage_ask_limit_volume,
                avarage_bids_volume=volumes.avarage_bid_limit_volume,
                nonce=volumes.nonce )
            await self.usdt_repo.add(history_record)

            return True

        except Exception as e:
            print(f"❌ Error saving volumes: {e}")
            return False

    async def get_usdt_limits_for_period(
            self,
            symbol: str,
            period_minutes: int
    ) -> list[OrderBookVolumesHistoryUsdt]:

        cutoff_timestamp = int((datetime.now() - timedelta(minutes=period_minutes)).timestamp())

        result = await self.usdt_repo.get_for_period(symbol,cutoff_timestamp)
        return result

    async def get_volumes_for_period(
            self,
            symbol: str,
            period_minutes: int
    ) -> List[OrderBookVolumesHistory]:

        cutoff_timestamp = int((datetime.now() - timedelta(minutes=period_minutes)).timestamp())

        result = await self.usdt_repo.get_for_period(symbol,cutoff_timestamp)
        return result.scalars().all()