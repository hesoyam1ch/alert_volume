import asyncio

import ccxt
import ccxt.pro as ccxtpro

from settings import DEVIATION_PERIOD_MINUTES
from src.services.common.logger import Logger
from src.services.helpers.order_book_handler import OrderBookHandler
from src.services.helpers.order_book_service import OrderBookService
from src.services.helpers.volume_deviation_service import VolumeDeviationDetector
from src.services.telegram_service import TelegramService


class MexcService:
    def __init__(self,order_book_service: OrderBookService,detector:VolumeDeviationDetector,telegram_service: TelegramService):
        self.logger: Logger = Logger("MexcService")
        self.client = ccxt.mexc()
        self.exchange_params = {
            'newUpdates': False,
            'options' : {
                "default_type": 'futures' }}
        self.order_book_service = order_book_service
        self.detector = detector
        self.telegram_service = telegram_service
        self.ws_client = ccxtpro.mexc(self.exchange_params)



    async def ws_ticker(self, symbol):
        self.logger.info(f"WS ticker: {symbol}")
        while True:
            try:
                ob = await self.ws_client.watch_order_book(symbol)
                volumes = OrderBookHandler.process_orderbook_second(ob)
                self.logger.info(f"{symbol} volumes calculated: {volumes}")
                saved = await self.order_book_service.save_volumes_usdt(volumes)
                self.logger.info(f"{symbol} volumes saved: {saved}")
                if not saved:
                    self.logger.info(f"WS ticker {symbol} was not saved")
                    return
                historical_data = await self.order_book_service.get_usdt_limits_for_period(
                    volumes.symbol,
                    DEVIATION_PERIOD_MINUTES
                )

                deviations = self.detector.detect_limits_deviations(volumes,historical_data)
                for deviation in deviations:
                    success = await self.telegram_service.send_deviation_alert(deviation)

                    if success:
                        self.logger.success(f"✅ Alert sent: {deviation.deviation_type.value} "
                                            f"for {deviation.symbol}")

                self.logger.info(f"{symbol} {ob['asks'][0]} {ob['bids'][0]}")
            except Exception as e:
                self.logger.error(f"{symbol} WS error: {e}")
                await asyncio.sleep(1)