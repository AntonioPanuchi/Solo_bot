"""
========================================
📋 ИНСТРУКЦИЯ ПО НАСТРОЙКЕ МОДУЛЯ
========================================

Этот модуль создает красивую веб-страницу для подключения VPN на разных устройствах.
Пользователи смогут легко подключить свои телефоны, компьютеры и даже телевизоры.

🔧 ШАГ 1: УСТАНОВКА
   Папка модуля уже находится в правильном месте (modules/xui_subpage/)

📝 ШАГ 2: НАСТРОЙКА
   Отредактируйте настройки ниже под свои нужды

🌐 ШАГ 3: НАСТРОЙКА ВЕБА (NGINX)
   Откройте файл настроек Nginx:
   sudo nano /etc/nginx/sites-available/default
   
   Добавьте этот блок в секцию server {}:
   location /connect/ {
       proxy_pass http://localhost:3023/connect/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   ВАЖНО: Замените 3023 на ваш MODULE_PORT, если меняли его ниже

🌐 ШАГ 3 (АЛЬТЕРНАТИВА): НАСТРОЙКА ВЕБА (CADDY)
   Если используете Caddy вместо Nginx, откройте:
   sudo nano /etc/caddy/Caddyfile
   
   Добавьте:
   reverse_proxy /connect/* http://localhost:3023
   ВАЖНО: Замените 3023 на ваш MODULE_PORT, если меняли его ниже

✅ ШАГ 4: ПРИМЕНЕНИЕ ИЗМЕНЕНИЙ
   Для Nginx: sudo nginx -t && sudo systemctl reload nginx
   Для Caddy: sudo systemctl reload caddy

🚀 ШАГ 5: ПЕРЕЗАПУСК БОТА
   sudo systemctl restart bot.service
   
   После этого в боте появится новая кнопка подключения устройств!
"""

# ========================================
# 🔧 ОСНОВНЫЕ НАСТРОЙКИ
# ========================================

# Включен ли модуль?
# True = работает новая красивая страница подключения
# False = остаются старые кнопки без изменений
MODULE_ENABLED = True

# Какие кнопки показывать в боте?
# "webapp" = только одна кнопка "Подключить устройство" (современные телефоны)
# "both" = две кнопки: "Подключить устройство" + "Другой способ" (для устройств, которые не поддерживают WebApp)
BUTTON_MODE = "both"

# На каком порту запускать веб-страницу?
# Обычно 3023 подходит для всех. Меняйте только если порт уже занят (также сменить надо будет в Nginx/Caddy)
MODULE_PORT = 3023

# Адрес страницы подключения
# Должен совпадать с настройкой в Nginx/Caddy выше. Обычно не нужно менять
BASE_PATH = "/connect/"

# ========================================
# 📝 ТЕКСТЫ НА КНОПКАХ
# ========================================
# Что будет написано на кнопках в боте

CONNECT_DEVICE_WEB = "📲 Подключить устройство"      # Основная кнопка, которая заменяется
CONNECT_DEVICE_EXTRA = "Другой способ подключения"   # Дополнительная кнопка со старой логикой (запасная для устройств, не поддерживающих WebApp)

# ========================================
# 🌍 ЯЗЫКОВЫЕ НАСТРОЙКИ
# ========================================
# Какой язык показывать пользователям на странице подключения

# Как определять язык пользователя?
# "user" = автоматически по языку Telegram пользователя (рекомендуется)
# "ru" = всегда показывать русский язык
# "en" = всегда показывать английский язык
LANGUAGE_MODE = "user"

# Какой язык использовать, если не получилось определить язык пользователя?
# Обычно "ru" подходит для большинства случаев
FALLBACK_LANGUAGE = "ru"

# ========================================
# 🎨 ВНЕШНИЙ ВИД И ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# ========================================

# Какую тему оформления использовать?
# "dark" = темная тема
# "light" = светлая тема
# "cyberpunk" = неоновая киберпанк тема
# "ocean" = морская голубая тема
# "fox" = оранжевая "лисья" тема
CURRENT_THEME = "dark"

# ========================================
# 📱 КАКИЕ ПРИЛОЖЕНИЯ ПОКАЗЫВАТЬ ПОЛЬЗОВАТЕЛЯМ
# ========================================
# Здесь настраивается, какие VPN-приложения предлагать для каждого типа устройства
# 0 = приложение скрыто
# 1, 2, 3... = порядок показа (1 = первое, 2 = второе и т.д.)
#
# РЕКОМЕНДАЦИИ:
# - Happ - рекомендованное приложение, можно ставить первым
# - Shadowrocket - платное, но очень хорошее для iOS/Mac на M1-M4
# - Hiddify - классика
# - V2rayTun - как альтернатива Happ
# - Streisand - только для iOS, но мало кто использует
# - Koala Clash - выручает на проблемной Windows 10 (по умолчанию скрыто, для подключения нужно настроить поддержку Clash в 3X-UI)

APPS_ENABLED = {
    "ios": {"Happ": 1, "V2rayTun": 2, "Shadowrocket": 3, "Streisand": 4},         # iPhone/iPad
    "android": {"Happ": 1, "Hiddify": 2, "V2rayTun": 3},                           # Android телефоны
    "windows": {"Happ": 1, "Hiddify": 2, "V2rayTun": 3, "Koalaclash": 4},         # Windows компьютеры
    "macos": {"Happ": 1, "Hiddify": 2, "Shadowrocket": 3, "V2rayTun": 4, "Koalaclash": 5},        # Mac компьютеры
    "linux": {"Hiddify": 1, "Happ": 2},                                           # Linux компьютеры
    "appletv": {"Happ": 1},                                                       # Apple TV
    "androidtv": {"Happ": 1}                                                      # Android TV
}

# ========================================
# 🔘 КАКИЕ КНОПКИ СКАЧИВАНИЯ ПОКАЗЫВАТЬ
# ========================================
# Для каждого приложения может быть несколько вариантов скачивания
# 
# 0 = кнопка скрыта
# 1, 2, 3... = порядок показа кнопок (1 = первая, 2 = вторая)

BUTTONS_ENABLED = {
    "ios": {                                        # iPhone/iPad
        "happ_1": 1, "happ_2": 2,                   # Happ: русский App Store (1) + мировой App Store (2)
        "v2raytun_1": 1,                            # V2rayTun: App Store
        "shadowrocket_1": 1,                        # Shadowrocket: App Store
        "streisand_1": 1                            # Streisand: App Store
    },
    "android": {                                    # Android телефоны
        "happ_1": 1, "happ_2": 2,                   # Happ: Google Play (1) + APK файл (2)
        "hiddify_1": 1,                             # Hiddify: APK файл
        "v2raytun_1": 1, "v2raytun_2": 2           # V2rayTun: Google Play (1) + APK файл (2)
    },
    "windows": {                                    # Windows компьютеры
        "happ_1": 1,                                # Happ: установщик exe
        "hiddify_1": 1,                             # Hiddify: установщик exe
        "v2raytun_1": 1,                            # V2rayTun: установщик exe
        "koalaclash_1": 1                           # Koala Clash: установщик exe
    },
    "macos": {                                      # Mac компьютеры
        "happ_1": 1, "happ_2": 2,                   # Happ: App Store (1) + файл для Intel (2)
        "hiddify_1": 1,                             # Hiddify: DMG файл
        "v2raytun_1": 1,                            # V2rayTun: App Store
        "shadowrocket_1": 1,                        # Shadowrocket: App Store
        "koalaclash_1": 1                           # Koala Clash: DMG файл
    },
    "linux": {                                      # Linux компьютеры
        "hiddify_1": 1,                             # Hiddify: AppImage файл
        "happ_1": 1                                 # Happ: AppImage файл
    },
    "appletv": {"happ_1": 1},                      # Apple TV: только Happ
    "androidtv": {"happ_1": 1}                     # Android TV: только Happ
}

# ========================================
# 📥 ССЫЛКИ ДЛЯ СКАЧИВАНИЯ ПРИЛОЖЕНИЙ
# ========================================
# Здесь указаны прямые ссылки на магазины и сайты для скачивания приложений
# Пользователи увидят кнопки "Скачать" с этими ссылками
# 
# ВНИМАНИЕ: Ссылки могут устареть! Периодически проверяйте их актуальность
# Если какая-то ссылка не работает, найдите новую

APP_LINKS = {
    # === iPhone и iPad ===
    "ios": {
        "happ_1": "https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973",      # Happ (русский App Store)
        "happ_2": "https://apps.apple.com/us/app/happ-proxy-utility/id6504287215",          # Happ (мировой App Store)
        "v2raytun_1": "https://apps.apple.com/ru/app/v2raytun/id6476628951",                # V2rayTun
        "shadowrocket_1": "https://apps.apple.com/ru/app/shadowrocket/id932747118",          # Shadowrocket (платное)
        "streisand_1": "https://apps.apple.com/us/app/streisand/id6450534064"                # Streisand
    },
    
    # === Android телефоны ===
    "android": {
        "happ_1": "https://play.google.com/store/apps/details?id=com.happproxy",                                                    # Happ (Google Play)
        "happ_2": "https://github.com/Happ-proxy/happ-android/releases/latest/download/Happ_beta.apk",                            # Happ (прямая ссылка APK)
        "hiddify_1": "https://github.com/hiddify/hiddify-next/releases/download/v2.5.7/Hiddify-Android-universal.apk",           # Hiddify APK
        "v2raytun_1": "https://play.google.com/store/apps/details?id=com.v2raytun.android",                                       # V2rayTun (Google Play)
        "v2raytun_2": "https://github.com/ADDVPN/v2raytun/releases/download/v1.3/v2RayTun_universal_3_12_46.apk"                 # V2rayTun APK
    },
    
    # === Windows компьютеры ===
    "windows": {
        "happ_1": "https://github.com/Happ-proxy/happ-desktop/releases/latest/download/setup-Happ.x86.exe",                      # Happ установщик
        "hiddify_1": "https://github.com/hiddify/hiddify-next/releases/download/v2.5.7/Hiddify-Windows-Setup-x64.exe",          # Hiddify установщик
        "v2raytun_1": "https://storage.v2raytun.com/v2RayTun_Setup.exe",                                                        # V2rayTun установщик
        "koalaclash_1": "https://github.com/coolcoala/clash-verge-rev-lite/releases/latest/download/Koala.Clash_x64-setup.exe"  # Koala Clash установщик
    },
    
    # === Mac компьютеры ===
    "macos": {
        "happ_1": "https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973",                                          # Happ (App Store для M1-M4)
        "happ_2": "https://github.com/Happ-proxy/happ-desktop/releases/download/alpha_0.3.6/Happ.macOS.universal.app.tar.gz",   # Happ (файл для Intel)
        "hiddify_1": "https://github.com/hiddify/hiddify-next/releases/download/v2.5.7/Hiddify-MacOS.dmg",                     # Hiddify установщик
        "v2raytun_1": "https://apps.apple.com/ru/app/v2raytun/id6476628951",                                                    # V2rayTun (App Store)
        "shadowrocket_1": "https://apps.apple.com/ru/app/shadowrocket/id932747118",                                             # Shadowrocket для  (App Store для M1-M4)
        "koalaclash_1": "https://github.com/coolcoala/clash-verge-rev-lite/releases/latest/download/Koala.Clash_x64.dmg"        # Koala Clash DMG файл
    },
    
    # === Linux компьютеры ===
    "linux": {
        "hiddify_1": "https://github.com/hiddify/hiddify-next/releases/download/v2.5.7/Hiddify-Linux-x64.AppImage",           # Hiddify (универсальный файл)
        "happ_1": "https://github.com/Happ-proxy/happ-desktop/releases/download/alpha_0.3.7/Happ.linux.x86.AppImage"            # Happ (универсальный файл)
    }
}

# ========================================
# 🔗 ССЫЛКИ ДЛЯ АВТОМАТИЧЕСКОГО ДОБАВЛЕНИЯ ПОДПИСКИ
# ========================================
# Специальные ссылки, с помощью которых подписка автоматически добавляется в приложение
# Обычно не нужно менять - это стандартные адреса для каждого приложения

DEEPLINKS = {
    "happ": "happ://add/",                    # Ссылка для Happ
    "hiddify": "hiddify://import/",           # Ссылка для Hiddify
    "v2raytun": "v2raytun://import/",         # Ссылка для V2rayTun
    "shadowrocket": "shadowrocket://add/",    # Ссылка для Shadowrocket
    "streisand": "streisand://import/",       # Ссылка для Streisand
    "clash": "clash://install-config?url="    # Ссылка для Koala Clash
}

# ========================================
# ✅ НАСТРОЙКА ЗАВЕРШЕНА
# ========================================
# После изменения настроек не забудьте:
# 1. Сохранить файл (Ctrl+S)
# 2. Перезапустить бота: sudo systemctl restart bot.service


