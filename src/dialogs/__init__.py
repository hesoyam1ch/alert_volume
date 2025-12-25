from .user_menu.config_user_dialog import config_menu_dialog
from .user_menu.dialogs import start_dialog
from .user_menu.menu import user_menu_dialog


def include_dialogs():
    return [start_dialog,user_menu_dialog,config_menu_dialog]
