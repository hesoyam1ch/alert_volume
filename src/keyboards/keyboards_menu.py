from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Запустить бота", callback_data="start_bot"),
            InlineKeyboardButton(text="Сделать конфиг", callback_data="make_config"),
        ]
    ]
)
