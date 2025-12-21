from aiogram import Router

from filters.chat_type import ChatTypeFilter
from . import start


def setup_routers() -> Router:
    router = Router()
    router.message.filter(ChatTypeFilter(["private"]))
    router.include_router(start.router)

    return router
