import asyncio
from datetime import datetime
from typing import Optional
import pytz

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from database.models import Admin, Payment
from database.payments import get_last_payments
from logger import logger

from .settings import (
    NOTIFICATIONS_ENABLED,
    NOTIFY_NEW_USERS, 
    NOTIFY_PAYMENT_SUCCESS,
    NOTIFICATION_SEND_MODE,
    NOTIFICATION_CHANNEL_ID,
    NOTIFICATION_TOPIC_NEW_USERS,
    NOTIFICATION_TOPIC_PAYMENTS,
    NOTIFICATION_TOPIC_MESSAGES,
    NOTIFICATION_OTHER_BOT_TOKEN,
    MIN_PAYMENT_AMOUNT_NOTIFY,
    NOTIFICATION_TIMEZONE,
    NOTIFY_USER_MESSAGES,
)
from .texts import (
    NEW_USER_TEMPLATE,
    PAYMENT_SUCCESS_TEMPLATE,
    USER_MESSAGE_TEMPLATE,
    SOURCE_DESCRIPTIONS,
    SOURCE_EMOJI,
    PAYMENT_SYSTEM_NAMES,
    NAME_INFO_TEMPLATE,
    USERNAME_INFO_TEMPLATE,
)


async def handle_user_registration(
    user_id: int,
    username: str = None,
    first_name: str = None,
    last_name: str = None,
    source_code: str = None,
    source_type: str = "direct",
    session: AsyncSession = None,
    **kwargs
):
    if NOTIFICATIONS_ENABLED != "true" or NOTIFY_NEW_USERS != "true":
        return

    try:
        source_template = SOURCE_DESCRIPTIONS.get(source_type, "❓ Неизвестный источник")
        if "{code}" in source_template and source_code:
            source = source_template.format(code=source_code)
        else:
            source = source_template.replace(" ({code})", "").replace(" (ID: {code})", "")

        name_info = ""
        if first_name or last_name:
            name_parts = []
            if first_name:
                name_parts.append(first_name)
            if last_name:
                name_parts.append(last_name)
            name_info = NAME_INFO_TEMPLATE.format(name=" ".join(name_parts))

        username_info = ""
        if username:
            username_info = USERNAME_INFO_TEMPLATE.format(username=username)

        tz = pytz.timezone(NOTIFICATION_TIMEZONE)
        time = datetime.now(tz).strftime("%H:%M:%S")

        text = NEW_USER_TEMPLATE.format(
            user_id=user_id,
            name_info=name_info,
            username_info=username_info,
            source=source,
            time=time
        )

        await send_notification_to_admins(text, session, NOTIFICATION_TOPIC_NEW_USERS)
        
    except Exception as e:
        logger.error(f"[Notifications] Ошибка отправки уведомления о регистрации пользователя {user_id}: {e}")



async def handle_payment_success(
    user_id: int,
    amount: float,
    payment_system: str = None,
    username: str = None,
    first_name: str = None,
    last_name: str = None,
    session: AsyncSession = None,
    **kwargs
):
    if NOTIFICATIONS_ENABLED != "true" or NOTIFY_PAYMENT_SUCCESS != "true":
        return
        
    if amount < MIN_PAYMENT_AMOUNT_NOTIFY:
        return

    try:
        payment_system_name = PAYMENT_SYSTEM_NAMES.get(payment_system, payment_system or "Неизвестно")

        name_info = ""
        if first_name or last_name:
            name_parts = []
            if first_name:
                name_parts.append(first_name)
            if last_name:
                name_parts.append(last_name)
            name_info = NAME_INFO_TEMPLATE.format(name=" ".join(name_parts))

        username_info = ""
        if username:
            username_info = USERNAME_INFO_TEMPLATE.format(username=username)

        tz = pytz.timezone(NOTIFICATION_TIMEZONE)
        time = datetime.now(tz).strftime("%H:%M:%S")

        text = PAYMENT_SUCCESS_TEMPLATE.format(
            amount=amount,
            payment_system=payment_system_name,
            user_id=user_id,
            name_info=name_info,
            username_info=username_info,
            time=time
        )

        await send_notification_to_admins(text, session, NOTIFICATION_TOPIC_PAYMENTS)
        
    except Exception as e:
        logger.error(f"[Notifications] Ошибка отправки уведомления об успешной оплате от пользователя {user_id}: {e}")


async def handle_user_message(
    user_id: int,
    message_text: str,
    username: str = None,
    first_name: str = None,
    last_name: str = None,
    session: AsyncSession = None,
    **kwargs
):
    if NOTIFICATIONS_ENABLED != "true" or NOTIFY_USER_MESSAGES != "true":
        return

    try:
        name_info = ""
        if first_name or last_name:
            name_parts = []
            if first_name:
                name_parts.append(first_name)
            if last_name:
                name_parts.append(last_name)
            name_info = NAME_INFO_TEMPLATE.format(name=" ".join(name_parts))

        username_info = ""
        if username:
            username_info = USERNAME_INFO_TEMPLATE.format(username=username)

        tz = pytz.timezone(NOTIFICATION_TIMEZONE)
        time = datetime.now(tz).strftime("%H:%M:%S")

        display_message = message_text

        text = USER_MESSAGE_TEMPLATE.format(
            user_id=user_id,
            name_info=name_info,
            username_info=username_info,
            message=display_message,
            time=time
        )

        await send_notification_to_admins(text, session, NOTIFICATION_TOPIC_MESSAGES)
        
    except Exception as e:
        logger.error(f"[Notifications] Ошибка отправки уведомления о сообщении от пользователя {user_id}: {e}")


async def send_notification_to_admins(text: str, session: AsyncSession, topic_id: str = None):
    from bot import bot
    
    async def send_to_admins_via_bot(bot_instance, session):
        result = await session.execute(select(Admin.tg_id))
        admin_ids = [row[0] for row in result.all()]
        
        if not admin_ids:
            logger.warning("[Notifications] В БД нет админов для отправки уведомлений")
            return
            
        for admin_id in admin_ids:
            try:
                await bot_instance.send_message(
                    chat_id=admin_id,
                    text=text,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
            except TelegramForbiddenError:
                logger.warning(f"[Notifications] Бот заблокирован администратором {admin_id}")
            except TelegramBadRequest as e:
                logger.error(f"[Notifications] Ошибка отправки администратору {admin_id}: {e}")
            except Exception as e:
                logger.error(f"[Notifications] Неожиданная ошибка отправки администратору {admin_id}: {e}")
            
            await asyncio.sleep(0.1)

    if not session:
        logger.error("[Notifications] Нет сессии БД для отправки уведомлений")
        return
        
    try:
        if NOTIFICATION_SEND_MODE == "bot":
            await send_to_admins_via_bot(bot, session)
            
        elif NOTIFICATION_SEND_MODE == "channel":
            channel_id = NOTIFICATION_CHANNEL_ID.strip()
            
            if not channel_id:
                logger.error("[Notifications] NOTIFICATION_CHANNEL_ID не задан для режима 'channel', fallback на bot")
                await send_to_admins_via_bot(bot, session)
                return
                
            send_kwargs = {"chat_id": channel_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}

            if topic_id:
                send_kwargs["message_thread_id"] = int(topic_id)
                
            try:
                await bot.send_message(**send_kwargs)
            except Exception as e:
                logger.error(f"[Notifications] Не удалось отправить в канал {channel_id}: {e}, fallback на bot")
                await send_to_admins_via_bot(bot, session)
                
        elif NOTIFICATION_SEND_MODE == "other_bot":
            if not NOTIFICATION_OTHER_BOT_TOKEN.strip():
                logger.error("[Notifications] NOTIFICATION_OTHER_BOT_TOKEN не задан для режима 'other_bot', fallback на bot")
                await send_to_admins_via_bot(bot, session)
                return
                
            other_bot = Bot(token=NOTIFICATION_OTHER_BOT_TOKEN)
            
            try:
                await send_to_admins_via_bot(other_bot, session)
            finally:
                await other_bot.session.close()
        else:
            logger.error(f"[Notifications] Неизвестный режим отправки: {NOTIFICATION_SEND_MODE}, fallback на bot")
            await send_to_admins_via_bot(bot, session)
            
    except Exception as e:
        logger.error(f"[Notifications] Критическая ошибка отправки уведомления: {e}")
        try:
            await send_to_admins_via_bot(bot, session)
        except Exception as fallback_error:
            logger.error(f"[Notifications] Ошибка fallback отправки: {fallback_error}")
