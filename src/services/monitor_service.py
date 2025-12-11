import asyncio

import ccxt as ccxt
import ccxt.pro as ccxtpro

from settings import DEVIATION_PERIOD_MINUTES
from src.services.helpers.order_book_handler import OrderBookHandler
from src.services.helpers.order_book_service import OrderBookService
from src.services.helpers.volume_deviation_service import VolumeDeviationDetector
from src.services.telegram_service import TelegramService

from src.database.db_client import DBClient
from src.services.common.logger import Logger


class MonitorService:
    def __init__(self,
                 db_client: DBClient,
                 order_book_service: OrderBookService,
                 volume_deviation_detector: VolumeDeviationDetector,
                 telegram_service: TelegramService):

        self.logger: Logger = Logger("MonitorService")
        self.client = ccxt.binance()
        self.exchange_params = {
            'newUpdates': False,
            'options' : {
                "default_type": 'spot' }}
        self.telegram = telegram_service
        self.db_client = db_client
        self.order_book_service = order_book_service
        self.detector = volume_deviation_detector
        self.ws_client = ccxtpro.binance(self.exchange_params)

    async def ws_ticker(self, symbol):
        self.logger.info(f"WS ticker: {symbol}")
        while True:
            try:
                ob = await self.ws_client.watch_order_book(symbol)
                self.logger.info(f"{symbol} {ob['asks'][0]} {ob['bids'][0]}")
                volumes = OrderBookHandler.process_orderbook(ob)
                self.logger.info(f"{symbol} volumes calculated: {volumes}")
                saved = await self.order_book_service.save_volumes(volumes)
                self.logger.info(f"{symbol} volumes saved: {saved}")
                if not saved:
                    self.logger.info(f"WS ticker {symbol} was not saved")
                    return
                historical_data = await self.order_book_service.get_volumes_for_period(
                    volumes.symbol,
                    DEVIATION_PERIOD_MINUTES
                )

                deviations = self.detector.detect_deviations(volumes,historical_data)
                for deviation in deviations:
                    success = await self.telegram.send_deviation_alert(deviation)

                    if success:
                        self.logger.success(f"✅ Alert sent: {deviation.deviation_type.value} "
                              f"for {deviation.symbol}")

            except Exception as e:
                self.logger.error(f"{symbol} WS error: {e}")
                await asyncio.sleep(1)

