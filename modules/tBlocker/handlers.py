from datetime import datetime
from typing import Optional
import pytz

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

from database.models import Admin, Key, User
from logger import logger

from .settings import (
    TBLOCKER_NOTIFICATIONS_ENABLED,
    NOTIFY_USER_TORRENT_BLOCK,
    NOTIFY_USER_TORRENT_UNBLOCK,
    NOTIFY_ADMIN_TORRENT_BLOCK,
    NOTIFY_ADMIN_TORRENT_UNBLOCK,
    ADMIN_NOTIFICATION_MODE,
    ADMIN_CHANNEL_ID,
    ADMIN_TOPIC_TORRENT_BLOCKS,
    OTHER_BOT_TOKEN,
    TIMEZONE,
    LOG_ALL_WEBHOOKS,
    SERVER_COUNTRIES,
)
from .texts import (
    TORRENT_BLOCKED_MSG,
    TORRENT_UNBLOCKED_MSG,
    ADMIN_TORRENT_BLOCKED_TEMPLATE,
    ADMIN_TORRENT_UNBLOCKED_TEMPLATE,
)


def get_country_from_server(server: str) -> str:
    server_clean = server.split(".")[0]

    if server in SERVER_COUNTRIES:
        return SERVER_COUNTRIES[server]

    for full_domain, country in SERVER_COUNTRIES.items():
        if server_clean in full_domain or server in full_domain:
            return country

    return server


def handle_telegram_errors(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except TelegramForbiddenError:
            tg_id = kwargs.get("tg_id") or args[1]
            logger.warning(f"🚫 Бот заблокирован пользователем {tg_id}.")
            return False
        except TelegramBadRequest:
            tg_id = kwargs.get("tg_id") or args[1]
            logger.warning(f"🚫 Чат не найден для пользователя {tg_id}.")
            return False
        except Exception as e:
            tg_id = kwargs.get("tg_id") or args[1]
            logger.error(f"❌ Ошибка отправки сообщения пользователю {tg_id}: {e}")
            return False

    return wrapper


@handle_telegram_errors
async def send_user_notification(tg_id: int, username: str, ip: str, server: str, action: str, duration: int = None, timestamp: str = None):
    if action == "block" and NOTIFY_USER_TORRENT_BLOCK != "true":
        return False
    if action == "unblock" and NOTIFY_USER_TORRENT_UNBLOCK != "true":
        return False

    from handlers.buttons import MAIN_MENU

    country = get_country_from_server(server)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=MAIN_MENU, callback_data="profile"))

    if action == "block":
        message = TORRENT_BLOCKED_MSG.format(
            username=username, 
            country=country, 
            duration=duration or "неизвестно"
        )
    else:
        message = TORRENT_UNBLOCKED_MSG.format(
            username=username, 
            country=country
        )

    from bot import bot
    await bot.send_message(
        chat_id=tg_id, 
        text=message, 
        parse_mode="HTML", 
        reply_markup=builder.as_markup()
    )
    return True


async def send_admin_notification(username: str, ip: str, server: str, action: str, duration: int = None, timestamp: str = None, session=None):
    if action == "block" and NOTIFY_ADMIN_TORRENT_BLOCK != "true":
        return
    if action == "unblock" and NOTIFY_ADMIN_TORRENT_UNBLOCK != "true":
        return

    if not session:
        logger.error(f"[Tblocker] Сессия БД не передана, невозможно получить список администраторов")
        return

    country = get_country_from_server(server)

    async def send_to_admins_via_bot(bot_instance, session):
        try:
            from sqlalchemy import select
            result = await session.execute(select(Admin.tg_id))
            admin_ids = [row[0] for row in result.fetchall()]
            
            if not admin_ids:
                return
                
            for admin_id in admin_ids:
                try:
                    await bot_instance.send_message(
                        chat_id=admin_id,
                        text=text,
                        parse_mode="HTML"
                    )
                except Exception as e:
                    logger.error(f"[Tblocker] Ошибка отправки уведомления админу {admin_id}: {e}")
                    
        except Exception as e:
            logger.error(f"[Tblocker] Ошибка получения списка администраторов: {e}")

    user_info = {}
    if session:
        try:
            from sqlalchemy import select

            key_result = await session.execute(
                select(Key.tg_id).where(Key.email == username)
            )
            key_row = key_result.fetchone()
            
            if key_row and key_row[0]:
                tg_id = key_row[0]

                user_result = await session.execute(
                    select(User.tg_id, User.username, User.first_name, User.last_name)
                    .where(User.tg_id == tg_id)
                )
                user_row = user_result.fetchone()
                
                if user_row:
                    user_info = {
                        "tg_id": user_row[0],
                        "username": user_row[1],
                        "first_name": user_row[2],
                        "last_name": user_row[3]
                    }
                    
        except Exception as e:
            logger.error(f"[Tblocker] Ошибка получения информации о пользователе: {e}")

    tz = pytz.timezone(TIMEZONE)
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            dt = dt.astimezone(tz)
            formatted_time = dt.strftime("%d.%m.%Y %H:%M:%S")
        except:
            formatted_time = timestamp
    else:
        formatted_time = datetime.now(tz).strftime("%d.%m.%Y %H:%M:%S")

    tg_id_info = ""
    if user_info.get("tg_id"):
        tg_id_info = f"• Telegram ID: <code>{user_info['tg_id']}</code>\n"
    
    username_info = ""
    if user_info.get("username"):
        username_info = f"• Username: @{user_info['username']}\n"
    
    name_info = ""
    name_parts = []
    if user_info.get("first_name"):
        name_parts.append(user_info["first_name"])
    if user_info.get("last_name"):
        name_parts.append(user_info["last_name"])
    if name_parts:
        name_info = f"• Имя: {' '.join(name_parts)}\n"

    if action == "block":
        text = ADMIN_TORRENT_BLOCKED_TEMPLATE.format(
            username=username,
            ip=ip,
            server=server,
            country=country,
            duration=duration or "неизвестно",
            timestamp=formatted_time,
            tg_id_info=tg_id_info,
            username_info=username_info,
            name_info=name_info
        )
    else:
        text = ADMIN_TORRENT_UNBLOCKED_TEMPLATE.format(
            username=username,
            ip=ip,
            server=server,
            country=country,
            timestamp=formatted_time,
            tg_id_info=tg_id_info,
            username_info=username_info,
            name_info=name_info
        )

    try:
        if ADMIN_NOTIFICATION_MODE == "bot":
            from bot import bot
            await send_to_admins_via_bot(bot, session)
            
        elif ADMIN_NOTIFICATION_MODE == "channel":
            channel_id = ADMIN_CHANNEL_ID.strip() if ADMIN_CHANNEL_ID else ""
            
            if not channel_id:
                from bot import bot
                await send_to_admins_via_bot(bot, session)
                return
                
            from bot import bot
            message_params = {
                "chat_id": channel_id,
                "text": text,
                "parse_mode": "HTML"
            }

            if ADMIN_TOPIC_TORRENT_BLOCKS:
                try:
                    topic_id = int(ADMIN_TOPIC_TORRENT_BLOCKS)
                    message_params["message_thread_id"] = topic_id
                except ValueError:
                    logger.warning(f"[Tblocker] Неверный формат ADMIN_TOPIC_TORRENT_BLOCKS: {ADMIN_TOPIC_TORRENT_BLOCKS}")
            
            try:
                await bot.send_message(**message_params)
            except Exception as e:
                logger.error(f"[Tblocker] Не удалось отправить в канал {channel_id}: {e}, fallback на bot")
                await send_to_admins_via_bot(bot, session)

        elif ADMIN_NOTIFICATION_MODE == "other_bot":
            if not OTHER_BOT_TOKEN.strip():
                from bot import bot
                await send_to_admins_via_bot(bot, session)
                return
                
            from aiogram import Bot
            other_bot = Bot(token=OTHER_BOT_TOKEN)
            
            try:
                await send_to_admins_via_bot(other_bot, session)
            except Exception as e:
                logger.error(f"[Tblocker] Ошибка отправки через другой бот: {e}, fallback на bot")
                from bot import bot
                await send_to_admins_via_bot(bot, session)
            finally:
                await other_bot.session.close()
        else:
            from bot import bot
            await send_to_admins_via_bot(bot, session)
            
    except Exception as e:
        logger.error(f"[Tblocker] Критическая ошибка отправки уведомления: {e}")
        try:
            from bot import bot
            await send_to_admins_via_bot(bot, session)
        except Exception as fallback_error:
            logger.error(f"[Tblocker] Ошибка fallback отправки: {fallback_error}")


async def tblocker_webhook_handler(request: web.Request):
    if TBLOCKER_NOTIFICATIONS_ENABLED != "true":
        return web.json_response({"status": "ok", "message": "module disabled"})

    try:
        data = await request.json()
        
        if LOG_ALL_WEBHOOKS == "true":
            logger.info(f"[Tblocker] Получен вебхук: {data}")

        username = data.get("username")
        ip = data.get("ip")
        server = data.get("server")
        action = data.get("action")
        duration = data.get("duration")
        timestamp = data.get("timestamp")

        if not all([username, ip, server, action]):
            logger.error("[Tblocker] Неполные данные в вебхуке")
            return web.json_response({"error": "Missing required fields"}, status=400)

        if action not in ["block", "unblock"]:
            logger.error(f"[Tblocker] Неизвестное действие: {action}")
            return web.json_response({"error": "Invalid action"}, status=400)

        sessionmaker = request.app["sessionmaker"]
        async with sessionmaker() as session:
            from database.keys import get_key_details
            key_info = await get_key_details(session, username)

            if not key_info:
                logger.error(f"[Tblocker] Ключ не найден для email {username}")
                return web.json_response({"error": "Key not found"}, status=404)

            tg_id = key_info["tg_id"]

            user_notification_success = await send_user_notification(
                tg_id=tg_id,
                username=username,
                ip=ip,
                server=server,
                action=action,
                duration=duration,
                timestamp=timestamp
            )

            if not user_notification_success:
                logger.warning(f"[Tblocker] Не удалось отправить уведомление пользователю {tg_id}")

            await send_admin_notification(
                username=username,
                ip=ip,
                server=server,
                action=action,
                duration=duration,
                timestamp=timestamp,
                session=session
            )

        return web.json_response({"status": "ok"})

    except Exception as e:
        logger.error(f"[Tblocker] Ошибка при обработке вебхука: {str(e)}", exc_info=True)
        return web.json_response({"error": str(e)}, status=500)
