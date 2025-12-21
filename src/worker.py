import asyncio

from src.database.db_client import DBClient
from src.services.exchanges.mexc_service import MexcService
from src.services.helpers.order_book_handler import OrderBookHandler
from src.services.helpers.order_book_service import OrderBookService
from src.services.helpers.volume_deviation_service import VolumeDeviationDetector
from src.services.monitor_service import MonitorService
from settings import SYMBOLS, DEVIATION_PERIOD_MINUTES, TRESHOLD_DEVIATION_PROCENTAGE, TELEGRAM_BOT_TOKEN, \
    TELEGRAM_CHAT_ID, UPPER_PERSENTAGE, LOWER_PERSENTAGE
from src.services.telegram_service import TelegramService


async def run_worker():
    db_client = DBClient()
    order_book_service = OrderBookService(db_client = db_client)
    volume_deviation_detector = VolumeDeviationDetector(period_minutes = DEVIATION_PERIOD_MINUTES,
                                                        threshold_percent = TRESHOLD_DEVIATION_PROCENTAGE,)

    telegram_service = TelegramService(bot_token = TELEGRAM_BOT_TOKEN,
                                       chat_id = TELEGRAM_CHAT_ID)


    monitor_service = MonitorService(db_client = db_client,
                                     order_book_service = order_book_service,
                                     volume_deviation_detector = volume_deviation_detector,
                                     telegram_service = telegram_service)

    mexc_service = MexcService(
        order_book_service = order_book_service,
        detector = volume_deviation_detector,
        telegram_service = telegram_service)

    tasks = [
        asyncio.create_task(mexc_service.ws_ticker(symbol))
        for symbol in SYMBOLS
    ]
    try:
        await asyncio.gather(*tasks)
    finally:
       await mexc_service.ws_client.close()
