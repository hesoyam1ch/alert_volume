from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.manager.manager import DialogManager
from aiogram import types
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.repositories.user_config_repository import UserConfigRepository
from src.states.dialog_states import UserConfigSG

async def process_symbol(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["symbol"] = message.text.upper()
    await message.answer(f"Символ токен обновлен: {message.text.upper()}")
    await dialog_manager.switch_to(UserConfigSG.config_menu)

async def process_threshold(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    try:
        threshold = float(message.text)
        dialog_manager.dialog_data["threshold"] = threshold
        await message.answer(f"Порог % обновлен: {threshold}%")
        await dialog_manager.switch_to(UserConfigSG.config_menu)
    except ValueError:
        await message.answer("Введите число без %")

async def process_period(message: types.Message, widget: MessageInput, dialog_manager: DialogManager):
    try:
        period = int(message.text)
        dialog_manager.dialog_data["deviation_period_minutes"] = period
        await message.answer(f"Период времени обновлен: {period} минут")
        await dialog_manager.switch_to(UserConfigSG.config_menu)
    except ValueError:
        await message.answer("Введите число в минутах!")

async def get_config_data(**kwargs):
    dialog_manager: DialogManager = kwargs["dialog_manager"]
    session: AsyncSession = kwargs["session"]
    user_repository = UserConfigRepository(session)

    data = dialog_manager.dialog_data

    if not data.get("symbol"):
        user = await user_repository.get_by_user_id(kwargs["event_from_user"].id)
        if user and user.symbol:
            data["symbol"] = user.symbol
            data["threshold"] = user.threshold_persentage
            data["deviation_period_minutes"] = user.deviation_period_minutes

    return {
        "symbol": data.get("symbol", "Не задано"),
        "threshold": data.get("threshold", "Не задано"),
        "period": data.get("deviation_period_minutes", "Не задано"),
    }

async def switch_to_symbol(c: types.CallbackQuery, widget, manager: DialogManager):
    await c.answer()
    await manager.switch_to(UserConfigSG.set_symbol)

async def switch_to_threshold(c: types.CallbackQuery, widget, manager: DialogManager):
    await c.answer()
    await manager.switch_to(UserConfigSG.set_threshold_persentage)

async def switch_to_period(c: types.CallbackQuery, widget, manager: DialogManager):
    await c.answer()
    await manager.switch_to(UserConfigSG.set_deviation_period_minutes)

async def go_back_to_menu(c: types.CallbackQuery, widget, manager: DialogManager):
    await c.answer()
    await manager.done()

async def refresh_config(c: types.CallbackQuery, widget, manager: DialogManager):
    data = manager.dialog_data

    if not data.get("symbol") or not data.get("threshold") or not data.get("deviation_period_minutes"):
        await c.answer("⚠️ Заполните все поля перед сохранением", show_alert=True)
        return

    session: AsyncSession = manager.middleware_data["session"]
    user_config_repository = UserConfigRepository(session)

    try:
        existing_config = await user_config_repository.get_by_user_id(c.from_user.id)

        if existing_config:
            existing_config.symbol = data["symbol"]
            existing_config.threshold_persentage = float(data["threshold"]) # need fix
            existing_config.deviation_period_minutes = int(data["deviation_period_minutes"])
            await session.commit()

        else:
            await user_config_repository.create_config(
                user_id=c.from_user.id,
                symbol=data["symbol"],
                threshold_percentage=float(data["threshold"]), #also need change
                deviation_period_minutes=int(data["deviation_period_minutes"])
            )

        await c.answer("✅ Конфиг сохранен!")
    except Exception as e:
        await session.rollback()
        await c.answer(f"❌ Ошибка сохранения: {str(e)}", show_alert=True)

config_menu_dialog = Dialog(
    Window(
        Format(
            "Твой конфиг:\n"
            "💠Symbol: {symbol}\n"
            "⚡ Threshold : {threshold} %\n"
            "⏱ Period : {period} минут\n\n"
            "Выбрать параметр для замены:"
        ),
        Row(
            Button(text=Const("Symbol"), id="change_symbol", on_click=switch_to_symbol),
            Button(text=Const("Threshold"), id="change_threshold", on_click=switch_to_threshold),
        ),
        Row(
            Button(text=Const("Period"), id="change_period", on_click=switch_to_period),
            Button(text=Const("Обновить"), id="refresh", on_click=refresh_config),
        ),
        Row(
            Button(text=Const("◀️ Назад в меню"), id="back_to_menu", on_click=go_back_to_menu),
        ),
        getter=get_config_data,
        state=UserConfigSG.config_menu
    ),
    Window(
        Const("Введите новый символ:"),
        MessageInput(process_symbol),
        Button(text=Const("◀️ Назад"), id="back", on_click=lambda c, w, m: m.switch_to(UserConfigSG.config_menu)),
        state=UserConfigSG.set_symbol
    ),
    Window(
        Const("Введите новый % threshold:"),
        MessageInput(process_threshold),
        Button(text=Const("◀️ Назад"), id="back", on_click=lambda c, w, m: m.switch_to(UserConfigSG.config_menu)),
        state=UserConfigSG.set_threshold_persentage
    ),
    Window(
        Const("Введите новый период n (минут):"),
        MessageInput(process_period),
        Button(text=Const("◀️ Назад"), id="back", on_click=lambda c, w, m: m.switch_to(UserConfigSG.config_menu)),
        state=UserConfigSG.set_deviation_period_minutes
    ),
)