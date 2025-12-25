from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button
from src.dialogs.user_menu.menu import start_process, configure_settings
from src.states.dialog_states import StartSG
from aiogram_dialog.widgets.text import Const


start_dialog = Dialog(
    Window(
        Const('👋 <b>Привет, я бот алерт по ордерам на мексе обращайся!</b>'),
        Row(
            Button(text=Const("Запустить бот"), id="start", on_click=start_process),
            Button(text=Const("Настроить конфиг"), id="configure", on_click=configure_settings),
        )
        ,
        state=StartSG.start,
    )
)