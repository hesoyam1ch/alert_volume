import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram import types
from aiogram_dialog import DialogManager

from src.states.dialog_states import StartSG

router = Router()
module_logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(StartSG.start)
