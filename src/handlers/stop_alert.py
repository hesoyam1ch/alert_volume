from aiogram import Router, types
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.user_config_repository import UserConfigRepository
from src.dialogs.user_menu import mexc_streams
from src.states.dialog_states import UserMenuSG

router = Router()

@router.message(Command("stop_alert"))
async def stop_alert_command(
    message: types.Message,
    dialog_manager: DialogManager,
):
    session: AsyncSession = dialog_manager.middleware_data["session"]
    user_id = message.from_user.id

    config = await UserConfigRepository(session).get_by_user_id(user_id)

    if not config:
        await message.answer("⚠️ Конфигурация не найдена")
        return

    stream = mexc_streams.get(config.symbol)

    if not stream:
        await message.answer("⚠️ Бот не запущен")
    else:
        await stream.remove_user(user_id)

        if not stream.subscribers:
            mexc_streams.pop(config.symbol, None)

        await message.answer("🛑 Бот остановлен")

    await dialog_manager.start(
        UserMenuSG.menu,
        mode=StartMode.RESET_STACK,
    )
