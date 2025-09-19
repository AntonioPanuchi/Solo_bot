import os
import threading
import uvicorn
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from hooks.hooks import register_hook
from .settings import MODULE_PORT, BASE_PATH

if not BASE_PATH.endswith('/'):
    BASE_PATH = BASE_PATH + '/'
from .api import create_api_routes
from .telegram import create_telegram_router, profile_menu_hook, view_key_menu_hook, key_creation_complete_hook

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "VERSION")
    try:
        with open(version_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "1.0.0"

router = create_telegram_router()
MODULE_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(MODULE_PATH, "static")

app = FastAPI(title="3X-UI Subscription Page", version=get_version())
create_api_routes(app, MODULE_PATH)
if os.path.exists(STATIC_PATH):
    app.mount(f"{BASE_PATH}static", StaticFiles(directory=STATIC_PATH), name="static")

def run_fastapi_server():
    try:
        uvicorn.run(app, host="0.0.0.0", port=MODULE_PORT, log_level="warning", access_log=False)
    except Exception as e:
        logging.error(f"[3X-UI Subscription Page] Ошибка запуска сервера: {e}")

server_thread = threading.Thread(target=run_fastapi_server, daemon=True)
server_thread.start()
register_hook("profile_menu", profile_menu_hook)
register_hook("view_key_menu", view_key_menu_hook)
register_hook("key_creation_complete", key_creation_complete_hook)
print("[3X-UI Subscription Page] Хуки зарегистрированы для замены кнопок")
