import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram import types
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from src.states.dialog_states import StartSG

router = Router()
module_logger = logging.getLogger(__name__)


@router.message(CommandStart(deep_link=False, magic=F.args.is_(None)))
async def start(message: types.Message, session: AsyncSession, dialog_manager: DialogManager) -> None:
    try:
        module_logger.info(f"User {message.from_user.first_name} started the bot")

        await dialog_manager.start(
            state=StartSG.start,
            mode=StartMode.RESET_STACK
        )
    except Exception as e:
        module_logger.error(f"Error in start handler: {e}")
        await message.answer("😔 Error. Try again later.")
