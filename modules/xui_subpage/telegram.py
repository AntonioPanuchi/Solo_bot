import logging
from aiogram import Router
from aiogram.types import InlineKeyboardButton, WebAppInfo
from config import WEBHOOK_HOST
from .settings import MODULE_ENABLED, BUTTON_MODE, CONNECT_DEVICE_WEB, CONNECT_DEVICE_EXTRA, BASE_PATH

if not BASE_PATH.endswith('/'):
    BASE_PATH = BASE_PATH + '/'

def create_telegram_router():
    router = Router()
    return router

def _create_connect_buttons(key_name, hook_name):
    buttons = []
    if not MODULE_ENABLED or not key_name:
        return buttons
    try:
        if BUTTON_MODE == "webapp":
            buttons.append({"remove_prefix": "connect_device|"})
            webapp_button = InlineKeyboardButton(text=CONNECT_DEVICE_WEB, web_app=WebAppInfo(url=f"{WEBHOOK_HOST}{BASE_PATH}?key_name={key_name}"))
            buttons.append({"insert_at": 0, "button": webapp_button})

        elif BUTTON_MODE == "both":
            buttons.append({"remove_prefix": "connect_device|"})
            webapp_button = InlineKeyboardButton(text=CONNECT_DEVICE_WEB, web_app=WebAppInfo(url=f"{WEBHOOK_HOST}{BASE_PATH}?key_name={key_name}"))
            callback_button = InlineKeyboardButton(text=CONNECT_DEVICE_EXTRA, callback_data=f"connect_device|{key_name}")
            buttons.append({"insert_at": 0, "button": webapp_button})
            buttons.append({"insert_at": 1, "button": callback_button})
        return buttons
    except Exception as e:
        logging.error(f"[3X-UI Subscription Page] Ошибка в {hook_name}: {e}")
        return buttons

async def profile_menu_hook(**kwargs):
    return []

async def view_key_menu_hook(**kwargs):
    return _create_connect_buttons(kwargs.get("key_name"), "view_key_menu_hook")

async def key_creation_complete_hook(**kwargs):
    return _create_connect_buttons(kwargs.get("key_name"), "key_creation_complete_hook")

def create_xui_subpage_buttons(key):
    buttons = []
    
    if not MODULE_ENABLED:
        return buttons
        
    try:
        key_name = getattr(key, 'email', '') or str(key)
        
        if BUTTON_MODE == "webapp":
            webapp_button = InlineKeyboardButton(
                text=CONNECT_DEVICE_WEB, 
                web_app=WebAppInfo(url=f"{WEBHOOK_HOST}{BASE_PATH}?key_name={key_name}")
            )
            buttons.append(webapp_button)
            
        elif BUTTON_MODE == "both":
            webapp_button = InlineKeyboardButton(
                text=CONNECT_DEVICE_WEB, 
                web_app=WebAppInfo(url=f"{WEBHOOK_HOST}{BASE_PATH}?key_name={key_name}")
            )
            callback_button = InlineKeyboardButton(
                text=CONNECT_DEVICE_EXTRA, 
                callback_data=f"connect_device|{key_name}"
            )
            buttons.extend([webapp_button, callback_button])
    except Exception as e:
        logging.error(f"[3X-UI Subscription Page] Ошибка создания кнопок для интеграции: {e}")
    
    return buttons