NEW_USER_TEMPLATE = """🆕 <b>Новый пользователь</b>

👤 <b>ID:</b> <code>{user_id}</code>
{name_info}{username_info}
📍 <b>Источник:</b> {source}
🕐 <b>Время:</b> {time}"""

# Варианты источников для подстановки
SOURCE_DESCRIPTIONS = {
    "direct": "🔗 Прямая ссылка",
    "partner": "🤝 Партнерская программа (ID: {code})",
    "referral": "👥 Реферальная ссылка (ID: {code})",
    "coupon": "🎫 Купон ({code})",
    "gift": "🎁 Подарок ({code})",
    "utm": "📊 UTM-метка ({code})",
}

PAYMENT_SUCCESS_TEMPLATE = """💰 <b>Успешная оплата</b>

💵 <b>Сумма:</b> {amount}₽
🏦 <b>Система:</b> {payment_system}

👤 <b>ID:</b> <code>{user_id}</code>
{name_info}{username_info}
🕐 <b>Время:</b> {time}"""

USER_MESSAGE_TEMPLATE = """💬 <b>Сообщение от пользователя</b>

👤 <b>ID:</b> <code>{user_id}</code>
{name_info}{username_info}
📝 <b>Сообщение:</b> {message}
🕐 <b>Время:</b> {time}"""

# Шаблон для имени пользователя
NAME_INFO_TEMPLATE = "📝 <b>Имя:</b> {name}\n"

# Шаблон для username
USERNAME_INFO_TEMPLATE = "🔗 <b>Username:</b> @{username}\n"

SOURCE_EMOJI = {
    "direct": "🔗",
    "partner": "🤝", 
    "referral": "👥",
    "coupon": "🎫",
    "gift": "🎁",
    "utm": "📊",
}

PAYMENT_SYSTEM_NAMES = {
    "kassai": "KassaAI",
    "kassai_plus": "KassaAI Plus",
    "robokassa": "RoboKassa",
    "yookassa": "ЮKassa", 
    "yoomoney": "ЮMoney",
    "freekassa": "FreeKassa",
    "cryptobot": "CryptoBot",
    "heleket": "Heleket",
    "stars": "Telegram Stars",
    "tribute": "Tribute",
    "wata": "WATA",
}
