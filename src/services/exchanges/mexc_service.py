import asyncio
import ccxt.pro as ccxtpro

from src.services.helpers.order_book_handler import OrderBookHandler
from src.services.helpers.order_book_service import OrderBookService


class MexcService:
    def __init__(self, symbol: str, order_book_service: OrderBookService):
        self.symbol = symbol
        self.order_book_service = order_book_service
        self.exchange_params = {
            'newUpdates': False,
            'options' : {
                "default_type": 'futures' }}
        self.ws_client = ccxtpro.mexc(self.exchange_params)
        self.subscribers: dict[int, callable] = {}
        self.task: asyncio.Task | None = None

    def add_user(self, user_id: int, callback, alert_service):
        self.subscribers[user_id] = {
            "callback": callback,
            "alert_service": alert_service,
            "notified": False,
        }

        if not self.task:
            self.task = asyncio.create_task(self._run())

    async def remove_user(self, user_id: int):
        self.subscribers.pop(user_id, None)

        if not self.subscribers and self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            self.task = None

    async def _run(self):
        try:
            while True:
                ob = await self.ws_client.watch_order_book(self.symbol)
                volumes = OrderBookHandler.process_orderbook_second(ob)
                await self.order_book_service.save_volumes_usdt(volumes)

                for user_id, data in self.subscribers.items():
                    if not data["notified"]:
                        await data["alert_service"].send_text(
                            f"✅ Подписка на <b>{self.symbol}</b> успешно запущена"
                        )
                        data["notified"] = True

                    asyncio.create_task(data["callback"](volumes))

        except ccxtpro.BaseError as e:
            for data in self.subscribers.values():
                await data["alert_service"].send_text(
                    f"❌ Ошибка подписки на <b>{self.symbol}</b>\n"
                    f"Проверь тикер или доступность рынка"
                )

        except asyncio.CancelledError:
            await self.ws_client.close()
            raise