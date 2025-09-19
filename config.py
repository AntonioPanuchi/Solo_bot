# Настройки авторизации
CLIENT_CODE = "awhatson"  # Уникальный код клиента (берется в личном кабинете на сайте, вкладка "Актуальные файлы")
CLIENT_PASSWORD = "Ewqdsacxz15"  # Пароль от учетной записи на сайте для проверки подлинности

# Основные настройки бота
PROJECT_NAME = "ROX.VPN"  # Имя вашего сервиса (отображается в боте и сообщениях)
USERNAME_BOT = "RX_VPN_Seller_bot"  # Имя бота в Telegram (без @, например, SoloNet для @SoloNet)
API_TOKEN = "7516503162:AAFHsj8c8a9mKf4WuvJETG-L3jjCdncCSn4"  # API-ключ бота (получается в @BotFather через /newbot)
BOT_SERVICE = "bot.service"  # Имя системного сервиса бота
LOG_ROTATION_TIME = "00:00"  # Периодичность создания файла логов

# Доступ к панели 3X-UI
ADMIN_USERNAME = "aw775hats0on"  # Логин администратора для панели 3X-UI (должен быть одинаковым для всех панелей)
ADMIN_PASSWORD = "fbhWjpZWw9a6TmaeRKP4YV98K8Rcmm3BSPHs1ujXGkJEK6bYC1IkBuK0hECiLtHV"  # Пароль администратора для панели 3X-UI (должен быть одинаковым для всех панелей)
USE_XUI_TOKEN = False  # Включение токена для входа в панель 3x-ui
XUI_TOKEN = ""  # Токен для 3x-ui (если USE_XUI_TOKEN = True)

# Логин и пароль от панели RemnaWave
REMNAWAVE_LOGIN = ""  # Логин администратора для панели Remnawave
REMNAWAVE_PASSWORD = ""  # Пароль администратора для панели Remnawave
REMNAWAVE_TOKEN_LOGIN_ENABLED = True  # Включение входа по токену ВМЕСТО логина и пароля
REMNAWAVE_ACCESS_TOKEN = ""  # Токен входа в панель Remnawave

# Подключение к базе данных
DB_NAME = "rbot_bd_name"  # Имя базы данных
DB_USER = "rbot_db"  # Логин пользователя базы данных
DB_PASSWORD = "O7zvJUl7rLAV6f9FGOqyHfEgrWcvXe5ThwRCUrRoR58xFUlbk"  # Пароль пользователя базы данных
PG_HOST = "localhost"  # Адрес сервера PostgreSQL (менять не рекомендуется)
PG_PORT = "5432"  # Порт сервера PostgreSQL (менять не рекомендуется)
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}"  # Полная строка подключения (формируется автоматически, не меняйте вручную)

# Настройки бекапов базы данных
BACK_DIR = "/root/backup"  # Путь к папке для хранения бекапов (создайте папку заранее и дайте права на запись)
BACKUP_TIME = 86400  # Интервал создания бекапов в секундах (21600 = 6 часов)

# Режим отправки бэкапов:
# - "default" — отправка всем администраторам через текущего бота (как сейчас).
# - "channel" — отправка в указанный канал или группу. Обязательно добавить бота в канал/группу и выдать ему права администратора.
# - "bot" — отправка через другого бота. Необходимо указать токен другого бота.
BACKUP_SEND_MODE = "default"  # Возможные значения: "default", "channel", "bot"

# Подпись (caption) к сообщению с бэкапом.
# Может использоваться как хэштег (например: "#backup") или просто как произвольный текст.
# Это поле необязательное — если оставить пустым, сообщение будет отправлено без подписи.
# Можно комбинировать хэштеги и текст: "#backup Автоматический бэкап базы"
BACKUP_CAPTION = ""

# ID канала/группы, если выбран режим "channel". Узнать ID @username_to_id_bot
# Указывается строкой, например: "-1001234567890".
# Обязательно: бот должен быть добавлен в канал и иметь права администратора.
BACKUP_CHANNEL_ID = ""

# ID топика (треда) внутри супергруппы, если нужно отправлять сообщение в определённый топик.
# Указывается строкой. 
# ❗ Важно: данный параметр работает **только для супергрупп с включёнными темами**.
BACKUP_CHANNEL_THREAD_ID = ""

# Токен другого бота, если выбран режим "bot".
# Указывается строкой. Необходимо указать токен другого бота.
BACKUP_OTHER_BOT_TOKEN = ""

# Настройки вебхуков и ссылок
WEBHOOK_HOST = "https://rbot.rox-net.ru"  # Домен вашего бота (например, https://store.domain.com)
WEBHOOK_PATH = "/webhook/"  # Путь для вебхука (менять не рекомендуется)
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"  # Полная ссылка на вебхук (формируется автоматически, не меняйте)
WEBAPP_HOST = "0.0.0.0"  # Адрес для запуска веб-приложения (менять не рекомендуется)
WEBAPP_PORT = 3001  # Порт для работы сервиса (менять не рекомендуется)
APP_URL = WEBHOOK_HOST  # Системная ссылка на сервис (менять не рекомендуется)
SUB_PATH = "/r_vpn_sub_jyye6638/"  # Путь для ссылки на подписку (сделайте красивым, должен совпадать с настройками в nginx)
PUBLIC_LINK = f"{WEBHOOK_HOST}{SUB_PATH}"  # Публичная ссылка на подписку (формируется автоматически, не меняйте)
REDIRECT_LINK = "https://t.me/RX_VPN_Seller_bot"  # Ссылка на страницу после успешной оплаты (можно указать ссылку на бота или внешний сайт)

## Управление API (доступно по адресу API_HOST/api/docs)
API_ENABLE = True  # Включение API и документации
API_HOST = "127.0.0.1"  # Адрес
API_PORT = 3003  #  Порт для API
API_LOGGING = True  # Включение логов

# Ссылки на приложения и подключение
DOWNLOAD_IOS = "https://apps.apple.com/ru/app/v2raytun/id6476628951"  # Ссылка на скачивание приложения для iOS
DOWNLOAD_ANDROID = "https://play.google.com/store/apps/details?id=com.v2raytun.android&hl=ru"  # Ссылка на скачивание приложения для Android
DOWNLOAD_PC = "https://github.com/hiddify/hiddify-next/releases/download/v2.5.7/Hiddify-Windows-Setup-x64.exe"  # Ссылка на скачивание приложения для Windows
DOWNLOAD_MACOS = "https://apps.apple.com/ru/app/v2raytun/id6476628951"  # Ссылка на скачивание приложения для macOS
CONNECT_IOS = f"{APP_URL}/?url=v2raytun://import/"  # Ссылка для подключения на iOS (формируется автоматически)
CONNECT_ANDROID = f"{APP_URL}/?url=v2raytun://import-sub?url="  # Ссылка для подключения на Android (формируется автоматически)
CONNECT_WINDOWS = f"{WEBHOOK_HOST}/?url=hiddify://import/"  # Ссылка для подключения на Windows (формируется автоматически)
CONNECT_MACOS = f"{WEBHOOK_HOST}/?url=v2raytun://import/"  # Ссылка для подключения на macOS (формируется автоматически)

# Платежные системы и быстрый флоу
# YooKassa
YOOKASSA_SHOP_ID = "1019565"  # ID магазина в YooKassa
YOOKASSA_SECRET_KEY = "live_QAch-WLZEyhAPAsG7LlUCfh09qTl29lVK32vfy5tsik"  # Секретный ключ YooKassa
VAT_CODE = 1 # Параметр для указания налогооблажнения, для самозанятых 1. 
EMAIL = "dggm.ru"  # Домен почты для чеков (например, solonet.ru, полную почту не указывать)
SERVICE_NAME = "Пополнение баланса ROX.VPN"  # Название услуги в чеке

# YooMoney
YOOMONEY_ID = "yoomoney_id"  # ID кошелька YooMoney
YOOMONEY_SECRET_KEY = "yoomoney_secret_key"  # Секретный ключ YooMoney
YOOMONEY_WEBAPP = True  # Включает режим WebApp для Юмани

# Robokassa
ROBOKASSA_LOGIN = "robokassa_login"  # Логин магазина в Robokassa
ROBOKASSA_PASSWORD1 = "robokassa_password1"  # Первый пароль Robokassa
ROBOKASSA_PASSWORD2 = "robokassa_password2"  # Второй пароль Robokassa
ROBOKASSA_TEST_MODE = 0  # Режим тестирования Robokassa (0 — обычный режим, 1 — тестовый)

# Freekassa
FREEKASSA_SHOP_ID = ""  # ID магазина в Freekassa
FREEKASSA_SECRET1 = ""  # Первое секретное слово Freekassa (для формирования подписи платежной формы)
FREEKASSA_SECRET2 = ""  # Второе секретное слово Freekassa (для проверки данных после оплаты)

# Crypto Bot
CRYPTO_BOT_TOKEN = "cryptobottoken"  # Токен Crypto Bot (получается в @CryptoBot)

# Telegram Stars
RUB_TO_XTR = 2.32  # Курс Telegram Stars к рублям (например, 1 звезда = 2.32 рубля)
STARS_BOT_URL = "https://t.me/PremiumBot"

# WATA (https://wata.pro/api)
WATA_RU_TOKEN = ""      # Access Token для РФ кассы
WATA_SBP_TOKEN = ""      # Access Token для СБП кассы
WATA_INT_TOKEN = ""      # Access Token для международной кассы
FAIL_REDIRECT_LINK = "https://pocomacho.ru/fail.html"

# KassaAI (https://api.fk.life/v1/) 
# Пропишите в nginx/caddy путь kassai/webhook для получения платежей, для кассы нужно дописать политику использования бота в одном из меню.
KASSAI_API_KEY = ""  # API ключ KassaAI (получается в личном кабинете)
KASSAI_SECRET_KEY = ""  # Секретный ключ 2 нужен из FREEKASSA для проверки подписи вебхуков
KASSAI_DOMAIN = "moydomen.ru"  # Ваш домен для формирования email клиента
KASSAI_IP = ""  # IP сервера для передачи в KassaAI
KASSAI_SHOP_ID = "" #ID магазина во FreeKassa
KASSAI_SUCCESS_URL = "https://pocomacho.ru/success.html"  # URL редиректа при успешной оплате
KASSAI_FAILURE_URL = "https://pocomacho.ru/fail.html"  # URL редиректа при неудачной оплате

# Heleket (https://api.heleket.com/v1/)
HELEKET_MERCHANT_ID = ""  # Merchant ID Heleket (получается в личном кабинете)
HELEKET_API_KEY = ""  # API ключ Heleket (получается в личном кабинете)
HELEKET_SUCCESS_URL = "https://"  # URL редиректа при успешной оплате
HELEKET_RETURN_URL = "https://"  # URL для возврата на сайт
HELEKET_CALLBACK_URL = f"{WEBHOOK_HOST}/heleket/webhook"  # URL для вебхуков
HELEKET_CURRENCY_RATE = 50  # Курс USD к рублям для конвертации (1 USD = 50 RUB)

# Tribute (https://t.me/tribute)
TRIBUTE_LINK = "https://t.me/tribute/app?startapp=???"  # Ссылка на донат (из @Tribute → Донат)
TRIBUTE_API_KEY = "???"  # Ключ API из настроек, там же указать и вебхук домен_бота /tribute/webhook, также проставить путь в nginx/caddy
TRIBUTE_CURRENCY = "RUB"  # Валюта расчетов в Tribute


# Дополнительные функции оплаты
DONATIONS_ENABLE = False  # Включить возможность донатов в боте (True — да, False — нет)
CASHBACK = 0  # Процент кэшбека от пополнений (0 — выключен)
USE_NEW_PAYMENT_FLOW = ["YOOKASSA", ]  # Список платежных систем, использующих новый поток оплаты.
## Пример: ["STARS", "YOOKASSA", "ROBOKASSA", "TRIBUTE", "CRYPTOBOT", "YOOMONEY"] # или "STARS" - для одной системы, False - Отключено

MULTICURRENCY_ENABLE = False # Включение мультивалютности, False - старое меню при оплате, True - новое
FX_MARKUP = 0  # Наценка на платежи в валюте в процентах (например, 100 = 100%, 50 = 50%, 0 = без наценки)


## Централизованное включение/отключение провайдеров
PROVIDERS_ENABLED = {
    "YOOKASSA": True,
    "YOOMONEY": False,
    "ROBOKASSA": False,
    "KASSAI_CARDS": False,
    "KASSAI_SBP": False,
    "WATA_RU": False,
    "WATA_SBP": False,
    "TRIBUTE": False,
    "HELEKET": False,
    "CRYPTOBOT": False,
    "FREEKASSA": False,
    "WATA_INT": False,
    "STARS": False,
}


# Шаблон для ручного пополнения баланса
RENEWAL_PRICES = {
    "1": 100,  # 1 месяц — 100 рублей
    "3": 330,  # 3 месяца — 285 рублей
    "6": 680,  # 6 месяцев — 540 рублей
    "12": 1150,  # 12 месяцев — 1000 рублей
}


# Ограничения пользователей
TRIAL_TIME_DISABLE = False  # Отключить тестовую подписку (True — да, False — нет)

# Реферальная программа
CHECK_REFERRAL_REWARD_ISSUED = False  # Включить единоразовый бонус за рефералов (True — да, False — нет)
REFERRAL_BONUS_PERCENTAGES = {
    1: 0.25,  # 25% бонус за рефералов 1 уровня
    2: 0.10,  # 10% бонус за рефералов 2 уровня
    3: 0.06,  # 6% бонус за рефералов 3 уровня
    4: 0.05,  # 5% бонус за рефералов 4 уровня
    5: 0.04,  # 4% бонус за рефералов 5 уровня
}
# Если хотите выдавать по 50 рублей, то указывайте число не в процентах. Пример: 1: 50, .

# Сообщения в боте
NEWS_MESSAGE = "Приглашай друзей, получай больше!"  # Сообщение в профиле для пользователей с активной подпиской

# Администраторы бота
ADMIN_ID = [
    5633113697,
]  # Список ID администраторов (узнать ID можно через @getmyid_bot)

# Настройки уведомлений
NOTIFICATION_TIME = 900  # Интервал проверки уведомлений в секундах (900 = 15 минут)
NOTIFY_RENEW = True  # Автопродление подписки за 24 или 10 часов до окончания (True — да, False — нет)
NOTIFY_INACTIVE = 48  # Уведомлять неактивных пользователей каждые 24 часа
NOTIFY_DELETE_KEY = False  # Удалять подписку после истечения срока (True — да, False — нет)
NOTIFY_DELETE_DELAY = 0  # Отсрочка удаления подписки в минутах (0 — без отсрочки)
NOTIFY_RENEW_EXPIRED = True  # Продлевать подписку после истечения срока (True — да, False — нет)

NOTIFY_EXTRA_DAYS = 2  # Дополнительные дни для пробного периода
NOTIFY_INACTIVE_TRAFFIC = 6  # Проверка неактивного трафика через сколько часов после создания подписки
NOTIFY_HOT_LEADS = True  # Включает или отключает уведомления горячих лидов
HOT_LEAD_INTERVAL_HOURS = 24  # Раз в сколько часов отправить уведомление для горячих лидов
DISCOUNT_ACTIVE_HOURS = 24  # Срок действия скидки в часах

# Настройки кнопок и интерфейса
PING_TIME = 60  # Интервал проверки серверов в секундах
CONNECT_PHONE_BUTTON = False  # Заменить раздельное меню загрузок/подключений в карточке подписки на старый вариант (True — да, False — нет)
ENABLE_UPDATE_SUBSCRIPTION_BUTTON = True  # Показывать кнопку "Обновить подписку" в карточке (True — да, False — нет)
ENABLE_DELETE_KEY_BUTTON = True  # Показывать кнопку "Удалить подписку" в меню подписки (True — да, False — нет)
BALANCE_BUTTON = True  # Показывать кнопку "Баланс" в профиле (True — да, False — нет)
INSTRUCTIONS_BUTTON = False  # Показывать кнопку "Инструкции" в профиле (True — да, False — нет, в меню ключа остается)
INLINE_MODE = True  # Включить инлайн-режим для кнопок подарков и рефералов (True — да, False — нет). Не забываем включить инлайн-режим в @BotFather для бота.
TOGGLE_CLIENT = False  # Включить функцию заморозки подписки (True — да, False — нет)
GIFTS_PER_PAGE = 5  # Количество подарков на странице в меню "Мои подарки"
GIFT_BUTTON = True  # Включает кнопку подарков
REFERRAL_BUTTON = True  # Включает кнопку реферальной системы
TOP_REFERRAL_BUTTON = True  # Включает кнопку топа пригласивших
QRCODE = True  # Включает кнопку показа QR-Code подписки
REFERRAL_QR = True  # Включает кнопку QR-кода реферальной ссылки
SHOW_START_MENU_ONCE = True  # Делает приветственное меню одноразовым
HWID_RESET_BUTTON = False  # Включает кнопку сброса HWID в меню подписки
RENEW_BUTTON_BEFORE_DAYS = 1  # Появление кнопки продлить за сколько дней до окончания подписки

# Работа с каналом
CHANNEL_EXISTS = False  # Есть ли канал сервиса? (False — убирает упоминания о канале в боте)
CHANNEL_URL = "https://t.me/rxvpn"  # Ссылка на публичный канал сервиса
SUPPORT_CHAT_URL = "https://t.me/rx_support_77"  # Ссылка на бота или профиль поддержки
CHANNEL_ID = "@RX_VPN"  # айди канала для работы как с открытыми, так и закрытыми каналами.
CHANNEL_REQUIRED = False  # Обязательная подписка на канал для использования бота (True — да, False — нет)

# Капча
CAPTCHA_ENABLE = False  # Включить капчу для защиты от ботов (True — да, False — нет)

# Подписки
RANDOM_SUBSCRIPTIONS = False  # Включить перемешку стран в подписке.

# Режимы работы
SUPERNODE = False  # Включить режим "Суперноды" (True — да, False — нет)
USE_COUNTRY_SELECTION = True  # Включить выбор стран для подписки (True — да, False — нет)
DEV_MODE = False  # Режим разработчика (не включайте, если не знаете, что это)
DISABLE_DIRECT_START = False # Режим регистрации по ссылкам рефералов/купонов/меток и др. Обычный /start игнорируется.
