from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from src.states.dialog_states import StartSG

start_dialog = Dialog(
    Window(
        Const('👋 <b>Hello!</b>'),
        state=StartSG.start,
    ),
)
