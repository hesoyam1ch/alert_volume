from aiogram import Router

from . import start
from .stop_alert import router as stop_alert_router


def setup_routers() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(stop_alert_router)

    return router
