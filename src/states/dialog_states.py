from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    start = State()

class StopAlertSG(StatesGroup):
    stop_alert = State()

class UserMenuSG(StatesGroup):
    menu = State()

class UserConfigSG(StatesGroup):
    set_access_key = State()
    set_symbol = State()
    set_threshold_persentage = State()
    set_deviation_period_minutes = State()
    comfirm = State()
    config_menu = State()