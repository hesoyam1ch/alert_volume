from aiogram_dialog import Dialog, Window, StartMode
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.manager.manager import DialogManager
from aiogram import types
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.repositories.coin_stats_repository import CoinStatsRepository
from src.db.repositories.order_book_repository import OrderBookVolumesHistoryUsdtRepository
from src.db.repositories.user_config_repository import UserConfigRepository
from src.db.repositories.user_repository import UserRepository
from src.dialogs.user_menu import mexc_streams
from src.services.common.user_alert_service import UserAlertService
from src.services.exchanges.mexc_service import MexcService
from src.services.helpers.order_book_service import OrderBookService
from src.services.helpers.volume_deviation_service import VolumeDeviationDetector
from src.services.user_processor import UserProcessor
from src.states.dialog_states import UserMenuSG, UserConfigSG

async def start_process(c: types.CallbackQuery, widget, dialog_manager: DialogManager):
    await c.answer()
    session: AsyncSession = dialog_manager.middleware_data["session"]
    bot = dialog_manager.middleware_data["bot"]
    usdt_repo = OrderBookVolumesHistoryUsdtRepository(session)
    coin_repo = CoinStatsRepository(session)
    user_id = c.from_user.id
    config = await UserConfigRepository(session).get_by_user_id(user_id)

    volume_deviation_detector = VolumeDeviationDetector(period_minutes = config.deviation_period_minutes,
                                                        threshold_persentage = config.threshold_persentage)

    alert_service = UserAlertService(bot, user_id)

    processor = UserProcessor(
        detector=volume_deviation_detector,
        order_book_service=OrderBookService(usdt_repo,coin_repo),
        alert_service=UserAlertService(bot, user_id),
        period_minutes=config.deviation_period_minutes,
    )

    stream = mexc_streams.setdefault(
        config.symbol,
        MexcService(config.symbol, OrderBookService(usdt_repo, coin_repo)),
    )
    stream.add_user(user_id, processor.on_volumes,alert_service)

    await c.message.answer("Бот запущен")
    await dialog_manager.done()

async def stop_process(c: types.CallbackQuery, widget, dialog_manager: DialogManager):
    await c.answer()

    session: AsyncSession = dialog_manager.middleware_data["session"]
    user_id = c.from_user.id
    config = await UserConfigRepository(session).get_by_user_id(user_id)

    stream = mexc_streams.get(config.symbol)
    if not stream:
        await c.message.answer("⚠️ Бот не запущен")
        return

    await stream.remove_user(user_id)

    if not stream.subscribers:
        mexc_streams.pop(config.symbol, None)

    await c.message.answer("🛑 Бот остановлен")

async def configure_settings(c: types.CallbackQuery, widget, dialog_manager: DialogManager):
    await c.answer()
    session: AsyncSession = dialog_manager.middleware_data["session"]
    user_repository = UserRepository(session)
    await user_repository.register_user(user_id=c.from_user.id, username=c.from_user.username)
    await dialog_manager.start(UserConfigSG.config_menu, mode=StartMode.NORMAL)

user_menu_dialog = Dialog(
    Window(
        Const("Выбери действие:"),
        Row(
            Button(text=Const("Запустить бот"), id="start", on_click=start_process),
            Button(text=Const("Настроить конфиг"), id="configure", on_click=configure_settings),
        ),
        state=UserMenuSG.menu,
    )
)