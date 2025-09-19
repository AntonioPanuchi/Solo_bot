import logging
import os
from datetime import datetime, timezone
from fastapi import HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import SUPPORT_CHAT_URL, USERNAME_BOT, WEBHOOK_HOST, PROJECT_NAME, DATABASE_URL
from database.models import Key

from .settings import (
    APPS_ENABLED, DEEPLINKS, APP_LINKS, BUTTONS_ENABLED, CURRENT_THEME, LANGUAGE_MODE, FALLBACK_LANGUAGE, BASE_PATH
)

if not BASE_PATH.endswith('/'):
    BASE_PATH = BASE_PATH + '/'
from .texts import STATIC_TEXTS, DINAMIC_TEXTS

_module_engine = None
_module_session_maker = None

def get_module_session_maker():
    global _module_engine, _module_session_maker
    if _module_session_maker is None:
        _module_engine = create_async_engine(
            DATABASE_URL, 
            echo=False, 
            future=True, 
            pool_size=5, 
            max_overflow=10, 
            pool_timeout=15
        )
        _module_session_maker = async_sessionmaker(
            bind=_module_engine, 
            expire_on_commit=False, 
            class_=AsyncSession
        )
    return _module_session_maker

def get_all_texts(language="ru"):
    texts = {}
    texts.update(STATIC_TEXTS.get(language, STATIC_TEXTS["ru"]))
    texts.update(DINAMIC_TEXTS.get(language, DINAMIC_TEXTS["ru"]))
    return texts


def create_api_routes(app, module_path):

    @app.get(f"{BASE_PATH}", response_class=HTMLResponse)
    async def device_connector_index():
        html_path = os.path.join(module_path, "static", "index.html")
        if os.path.exists(html_path):
            with open(html_path, encoding="utf-8") as f:
                content = f.read()

            content = content.replace("{{PROJECT_NAME}}", PROJECT_NAME)
            content = content.replace("{{WEBHOOK_HOST}}", WEBHOOK_HOST)
            content = content.replace("{{SUPPORT_CHAT_URL}}", SUPPORT_CHAT_URL)
            content = content.replace("{{USERNAME_BOT}}", USERNAME_BOT)
            content = content.replace("{{BASE_PATH}}", BASE_PATH)

            return HTMLResponse(content=content)

        return HTMLResponse(content=f"<h1>Подключение устройства</h1><p>Модуль xui_subpage активирован для {PROJECT_NAME}</p>")

    @app.get(f"{BASE_PATH}api/sub")
    async def get_sub(key_name=Query(None), tg_id=Query(None)):

        if not key_name and tg_id is None:
            raise HTTPException(status_code=400, detail="Required key_name or tg_id parameter")
        if tg_id is not None:
            try:
                tg_id = int(tg_id)
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Invalid tg_id parameter")
        try:
            session_maker = get_module_session_maker()
            async with session_maker() as session:
                if key_name:
                    query = select(Key).where(
                        Key.email == key_name,
                        Key.is_frozen == False
                    ).order_by(Key.expiry_time.desc()).limit(1)
                else:
                    query = select(Key).where(
                        Key.tg_id == tg_id,
                        Key.is_frozen == False
                    ).order_by(Key.expiry_time.desc()).limit(1)
                
                result = await session.execute(query)
                row = result.scalar_one_or_none()

                if not row:
                    raise HTTPException(status_code=404, detail="Subscription not found")
                expiry_iso = datetime.fromtimestamp(row.expiry_time / 1000, timezone.utc).isoformat()
                remnawave_link = getattr(row, "remnawave_link", None)
                primary_link = row.key or remnawave_link
                return {
                    "key": row.key,
                    "expiry": expiry_iso,
                    "link": primary_link,
                    "email": getattr(row, "email", ""),
                }

        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"[3X-UI Subscription Page] Database error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @app.post(f"{BASE_PATH}auth/start")
    async def auth_start():
        return JSONResponse(content={"status": "ok"})

    @app.get(f"{BASE_PATH}api/settings")
    async def get_settings():
        return JSONResponse(content={
                "project_name": PROJECT_NAME, 
                "bot_username": USERNAME_BOT, 
                "support_chat": SUPPORT_CHAT_URL, 
                "webhook_host": WEBHOOK_HOST,
                "base_path": BASE_PATH,
                "color_theme": CURRENT_THEME,
                "language": {
                    "default_mode": LANGUAGE_MODE,
                    "fallback": FALLBACK_LANGUAGE
                },
                "apps": APPS_ENABLED,
                "deeplinks": DEEPLINKS,
                "app_links": APP_LINKS,
                "buttons": BUTTONS_ENABLED
            })

    @app.get(f"{BASE_PATH}health")
    async def health_check():
        try:
            session_maker = get_module_session_maker()
            async with session_maker() as session:
                await session.execute(select(1))
                db_status = "ok"
        except Exception:
            db_status = "unavailable"
        return JSONResponse(content={"status": "ok", "database": db_status, "module": "xui_subpage"})

    @app.get(f"{BASE_PATH}api/texts")
    async def get_texts(language: str = "ru"):
        texts = get_all_texts(language)
        return JSONResponse(content={"texts": texts, "language": language})

    @app.post(f"{BASE_PATH}api/tv")
    async def send_to_tv(request: Request):
        """Proxy endpoint for sending subscription to TV via Happ API"""
        try:
            import httpx
            
            data = await request.json()
            code = data.get("code")
            subscription_data = data.get("data")
            
            if not code or not subscription_data:
                return JSONResponse(
                    content={"success": False, "error": "Missing code or data parameter"}, 
                    status_code=400
                )
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://check.happ.su/sendtv/{code}",
                    headers={"Content-Type": "application/json"},
                    json={"data": subscription_data}
                )
                
                response_text = response.text

                if response.status_code == 200:
                    return JSONResponse(
                        content={
                            "success": True, 
                            "message": "Subscription sent successfully",
                            "response": response_text
                        }
                    )
                else:
                    return JSONResponse(
                        content={
                            "success": False,
                            "error": f"Happ API error: {response.status_code}",
                            "response": response_text
                        },
                        status_code=response.status_code
                    )
                    
        except Exception as e:
            logging.error(f"[TV API] Error sending to Happ API: {e}")
            return JSONResponse(
                content={"success": False, "error": str(e)},
                status_code=500
            )
