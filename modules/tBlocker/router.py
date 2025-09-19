from aiogram import Router
from .settings import TBLOCKER_WEBHOOK_PATH
from .handlers import tblocker_webhook_handler

router = Router(name="tblocker_notifications_module")


def get_webhook_data():
    return {
        "path": TBLOCKER_WEBHOOK_PATH,
        "handler": tblocker_webhook_handler
    }
