# ========================================
# ТЕКСТЫ ДЛЯ ИНТЕРФЕЙСА ПОДКЛЮЧЕНИЯ УСТРОЙСТВ
# ========================================
# Здесь настраиваются все тексты, которые видят пользователи на страничке подключения.

STATIC_TEXTS = {
    "ru": {
        # === ОСНОВНЫЕ ЭЛЕМЕНТЫ ИНТЕРФЕЙСА ===
        # Эти тексты появляются в главных частях странички
        "loading": "Загрузка...",                    # Показывается пока страница загружается (не видно за прелоадером)
        "installation": "Установка",                 # Заголовок раздела с инструкциями 
        "subscription_active": "Подписка активна",   # Статус когда всё работает
        
        # === ИНФОРМАЦИЯ О ПОДПИСКЕ ===
        # Показывает сколько времени осталось до окончания подписки
        "valid_until": "Осталось: загрузка...",      # Пока загружается информация (не видно за прелоадером)
        "valid_until_loading": "Осталось: загрузка...",  # Пока загружается информация (не видно за прелоадером)
        "valid_until_date": "Осталось:",            # Перед числом дней/часов/минут
        "expired": "Истекло",                       # Когда подписка закончилась
        "time_days": "д",                          # Сколько дней осталось
        "time_hours": "ч",                         # Сколько часов осталось
        "time_minutes": "м",                       # Сколько минут осталось
        
        # === НАЗВАНИЯ ПЛАТФОРМ ===
        # Список всех поддерживаемых платформ (менять нежелательно)
        "ios": "iOS",
        "android": "Android",
        "windows": "Windows",
        "macos": "macOS",
        "linux": "Linux",
        "appletv": "Apple TV",
        "androidtv": "Android TV",
        
        # === ЯЗЫКОВЫЕ НАСТРОЙКИ (не используются пока) ===
        
        # === ПРЕДУПРЕЖДЕНИЯ ===
        # Предупреждение для Windows пользователей об антивирусе
        # ВАЖНО: Чтобы убрать предупреждение, просто очистите текст: "antivirus_note": ""
        "antivirus_note": "Игнорируйте или отклоняйте уведомления от антивируса - это нормальное поведение для VPN программ.",
        
        # === TV ПОДКЛЮЧЕНИЕ ===
        # Тексты для подключения телевизоров через QR-код
        "androidtv_modal_title": "Подключение Android TV",
        "appletv_modal_title": "Подключение Apple TV",
        "tv_camera_instructions": "Направьте камеру на QR-код с телевизора",
        "tv_camera_error": "Не удалось получить доступ к камере",
        
        # === QR-СКАНИРОВАНИЕ ===
        # Статусы при сканировании QR-кодов с телевизора
        "qr_detected": "QR обнаружен",
        "qr_parse_error": "Не удалось распознать QR-код",
        "qr_code_not_found": "Код не найден",
        "sending_to_tv": "Отправляем на TV...",
        "subscription_sent_success": "Подписка отправлена на TV!",
        "no_subscription_link": "Нет ссылки подписки",
        "send_error": "Не удалось отправить подписку",
    },
    "en": {
        # === MAIN INTERFACE ELEMENTS ===
        # These texts appear in main parts of the page
        "loading": "Loading...",                     # Shown while page is loading (not visible behind the preloader)
        "installation": "Installation",              # Installation section title
        "subscription_active": "Subscription active", # Status when everything works
        
        # === SUBSCRIPTION INFO ===
        # Shows how much time is left before subscription expires
        "valid_until": "Remaining: loading...",      # While loading info (not visible behind the preloader)
        "valid_until_loading": "Remaining: loading...",   # While loading info (not visible behind the preloader)
        "valid_until_date": "Remaining:",            # Before number of days/hours/minutes
        "expired": "Expired",                       # When subscription ended
        "time_days": "d",                           # How many days are left
        "time_hours": "h",                          # How many hours are left
        "time_minutes": "m",                        # How many minutes are left
        
        # === DEVICE AND PLATFORM NAMES ===
        # List of all supported platforms (shouldn't be changed)
        "ios": "iOS",
        "android": "Android",
        "windows": "Windows",
        "macos": "macOS",
        "linux": "Linux",
        "appletv": "Apple TV",
        "androidtv": "Android TV",
        
        # === LANGUAGE SETTINGS (not used yet) ===
        
        # === WARNINGS ===
        # Warning for Windows users about antivirus
        # IMPORTANT: To remove warning, just clear the text: "antivirus_note": ""
        "antivirus_note": "Ignore or decline antivirus notifications - this is normal behavior for VPN programs.",
        
        # === TV CONNECTION ===
        # Texts for connecting TVs via QR code
        "androidtv_modal_title": "Android TV Connection",
        "appletv_modal_title": "Apple TV Connection",
        "tv_camera_instructions": "Point camera at QR code from TV",
        "tv_camera_error": "Could not access camera",
        
        # === QR SCANNING ===
        # Status messages when scanning QR codes from TV
        "qr_detected": "QR detected",
        "qr_parse_error": "Unable to recognize QR code",
        "qr_code_not_found": "Code not found",
        "sending_to_tv": "Sending to TV...",
        "subscription_sent_success": "Subscription sent to TV!",
        "no_subscription_link": "No subscription link",
        "send_error": "Failed to send subscription",
    },
}

# ========================================
# ТЕКСТЫ ДЛЯ ИНСТРУКЦИЙ И КНОПОК
# ========================================
# Здесь находятся подробные инструкции для каждого приложения и устройства.
# Эти тексты показываются пользователю пошагово: как скачать, установить и подключиться.
# Можно редактировать, но старайтесь сохранить понятность для обычных пользователей.

DINAMIC_TEXTS = {
    "ru": {
        # === ОСНОВНЫЕ ЗАГОЛОВКИ ШАГОВ ===
        "install_title": "Установите и откройте",        # Заголовок 1-го шага
        "add_subscription_title": "Добавьте подписку",   # Заголовок 2-го шага
        "connect_title": "Подключите и пользуйтесь",     # Заголовок 3-го шага
        
        # === ТЕКСТЫ КНОПОК И ССЫЛОК ===
        "download": "Скачать",                          # Универсальная кнопка скачивания
        "open_in_app_store": "Открыть в App Store",     # Кнопка для перехода в магазин Apple
        "open_in_google_play": "Открыть в Google Play", # Кнопка для перехода в магазин Google
        "open_in_app_store_mir": "Открыть в App Store [мир]",  # Глобальный магазин
        "open_in_app_store_rus": "Открыть в App Store [rus]",  # Российский магазин
        "for_m_series": "Для процессоров M-серии",            # Новые Mac с чипом M1-M4
        "for_intel": "Для Intel процессоров",                 # Старые Mac с Intel
        "add_subscription_button": "Добавить подписку",  # Текст на кнопке добавления подписки в программу
        "qr_tv_happ": "Отсканируйте QR-код",            # Кнопка для сканирования QR-кода на TV
     
        # === ИНСТРУКЦИИ ПО УСТАНОВКЕ ПРИЛОЖЕНИЙ ===
        # Для каждого приложения и платформы есть своя инструкция
        
        # HAPP
        "install_happ_ios": "Скачайте Happ с App Store и установите приложение. После установки запустите его и разрешите создание VPN-профиля.",
        "install_happ_android": "Скачайте Happ с Google Play или файл apk с официального сайта и установите приложение. После установки запустите его и разрешите создание VPN-соединения.",
        "install_happ_windows": "Скачайте Happ с официального сайта и установите приложение. После установки запустите его от имени администратора для корректной работы VPN.",
        "install_happ_macos": "Скачайте Happ с App Store (для M-серии) или с официального сайта (для Intel) и установите приложение. После установки запустите его и разрешите создание VPN-профиля.",
        "install_happ_linux": "Скачайте Happ для Linux с официального сайта. Установите пакет командой sudo dpkg -i happ.deb или через менеджер пакетов вашего дистрибутива.",
        "install_happ_appletv": "Установите приложение Happ на Apple TV через App Store. Откройте приложение и подготовьтесь к добавлению подписки через QR-код.",
        "install_happ_androidtv": "Установите приложение Happ на Android TV через Google Play. Откройте приложение и подготовьтесь к добавлению подписки через QR-код.",
        
        # V2RAYTUN
        "install_v2raytun_ios": "Скачайте v2RayTun с App Store и установите приложение. После установки запустите его и разрешите создание VPN-профиля.",
        "install_v2raytun_android": "Скачайте v2RayTun с Google Play или файл apk с официального сайта и установите приложение. После установки запустите его и разрешите создание VPN-соединения.",
        "install_v2raytun_windows": "Скачайте v2RayTun с официального сайта и установите приложение. После установки запустите его от имени администратора для корректной работы VPN.",
        "install_v2raytun_macos": "Скачайте v2RayTun с App Store и установите приложение. После установки запустите его и разрешите создание VPN-профиля.",
        
        # SHADOWROCKET
        "install_shadowrocket_ios": "Скачайте Shadowrocket с App Store и установите приложение. После установки запустите его и разрешите создание VPN-профиля.",
        "install_shadowrocket_macos": "Скачайте Shadowrocket с App Store и установите приложение. После установки запустите его и разрешите создание VPN-профиля.",
        
        # STREISAND
        "install_streisand_ios": "Скачайте Streisand с App Store и установите приложение. После установки запустите приложение и разрешите создание VPN-профиля.",
        
        # HIDDIFY
        "install_hiddify_android": "Скачайте Hiddify с официального сайта и установите приложение. После установки запустите приложение и разрешите создание VPN-соединения.",
        "install_hiddify_windows": "Скачайте Hiddify с официального сайта и установите приложение. После установки запустите его от имени администратора для корректной работы VPN.",
        "install_hiddify_macos": "Скачайте Hiddify с официального сайта и установите приложение. После установки запустите его и разрешите создание VPN-профиля.",
        "install_hiddify_linux": "Скачайте Hiddify для Linux с GitHub. Установите AppImage файл или используйте пакет для вашего дистрибутива.",

        # KOALA CLASH
        "install_koalaclash_macos": "Скачайте Koala Clash с официального сайта и установите приложение. После установки запустите его от имени администратора для корректной работы VPN.",
        "install_koalaclash_windows": "Скачайте Koala Clash с официального сайта и установите приложение. После установки запустите его от имени администратора для корректной работы VPN.",
        
        # === ИНСТРУКЦИИ ПО ДОБАВЛЕНИЮ ПОДПИСКИ ===
        "add_subscription_happ": "Нажмите кнопку ниже — приложение Happ откроется, и подписка добавится автоматически.<br><br>Если подписка не добавилась автоматически, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">скопируйте ссылку подписки</span> и добавьте ее в приложение вручную через кнопку «<b>+</b>» в правом верхнем углу → «Вставить из буфера обмена»",
        "add_subscription_hiddify": "Нажмите кнопку ниже — приложение Hiddify откроется, и подписка добавится автоматически.<br><br>Если подписка не добавилась автоматически, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">скопируйте ссылку подписки</span> и добавьте ее в приложение вручную через кнопку «<b>+</b>» в правом верхнем углу → «Добавить из буфера обмена»",
        "add_subscription_v2raytun": "Нажмите кнопку ниже — приложение V2rayTun откроется, и подписка добавится автоматически.<br><br>Если подписка не добавилась автоматически, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">скопируйте ссылку подписки</span> и добавьте ее в приложение вручную через кнопку «<b>+</b>» в правом верхнем углу → «Добавить из буфера»",
        "add_subscription_shadowrocket": "Нажмите кнопку ниже — приложение Shadowrocket откроется, и подписка добавится автоматически.<br><br>Если подписка не добавилась автоматически, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">скопируйте ссылку подписки</span> и добавьте ее в приложение вручную через кнопку «<b>+</b>» в правом верхнем углу → «Сохранить»",
        "add_subscription_streisand": "Нажмите кнопку ниже — приложение Streisand откроется, и подписка добавится автоматически.<br><br>Если подписка не добавилась автоматически, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">скопируйте ссылку подписки</span> и добавьте ее в приложение вручную через кнопку «<b>+</b>» в правом верхнем углу → «Добавить из буфера»",
        "add_subscription_koalaclash": "Нажмите кнопку ниже — приложение Koala Clash откроется, и подписка добавится автоматически.<br><br>Если подписка не добавилась автоматически, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">скопируйте ссылку подписки</span> и добавьте ее в приложение вручную через кнопку «Добавить профиль» на главной странице → «Импорт»",
        "add_subscription_tv": "Отсканируйте код с телевизора по кнопке ниже. Нужно будет разрешить использование камеры.",
        
        # === ИНСТРУКЦИИ ПО ПОДКЛЮЧЕНИЮ В ПРИЛОЖЕНИЯХ ===
        # Как включить VPN в каждом приложении после добавления подписки
        "connect_happ": "В приложении Happ выберите необходимый сервер из списка серверов и нажмите большую круглую кнопку включения VPN в верхней части экрана.",
        "connect_happ_appletv": "На Apple TV выберите необходимый сервер из списка серверов и нажмите большую круглую кнопку включения VPN.",
        "connect_happ_androidtv": "На Android TV выберите необходимый сервер из списка серверов и нажмите большую круглую кнопку включения VPN.",
        "connect_v2raytun": "В приложении v2RayTun выберите необходимый сервер из списка серверов и нажмите кнопку включения VPN в верхней части экрана.",
        "connect_shadowrocket": "В приложении Shadowrocket выберите необходимый сервер из списка серверов и нажмите переключатель в правой верхней части экрана для включения VPN.",
        "connect_streisand": "В приложении Streisand выберите необходимый сервер из списка серверов и нажмите кнопку включения VPN в верхней части экрана.",
        "connect_hiddify": "В приложении Hiddify нажмите кнопку подключения VPN. Также вы можете выбрать необходимый сервер из раздел «Профили»",
        "connect_koalaclash": "После добавления подписки программа может запросить установку службы TUN — установите. Далее выберите необходимый сервер из списка серверов и нажмите кнопку включения VPN для активации подключения.",
               
        # === УВЕДОМЛЕНИЯ ===
        "link_copied": "Ссылка скопирована",
        "failed_to_copy": "Не удалось скопировать"
    },
    "en": {
        # === MAIN STEP TITLES ===
        "install_title": "Install and open",              # Title of 1st step
        "add_subscription_title": "Add subscription",      # Title of 2nd step
        "connect_title": "Connect and Use",               # Title of 3rd step
        
        # === BUTTON AND LINK TEXTS ===
        "download": "Download",                          # Universal download button
        "open_in_app_store": "Open in App Store",     # Button to go to Apple store
        "open_in_google_play": "Open in Google Play", # Button to go to Google store
        "open_in_app_store_mir": "Open in App Store [global]", # Global store
        "open_in_app_store_rus": "Open in App Store [rus]",    # Russian store
        "for_m_series": "For M-series processors",            # New Macs with M1-M4 chip
        "for_intel": "For Intel processors",                  # Old Macs with Intel
        "add_subscription_button": "Add subscription",     # Text on the button for adding a subscription to the app
        "qr_tv_happ": "Scan QR code",                    # Button for scanning QR code on TV
                
        # === APP INSTALLATION INSTRUCTIONS ===
        # Each app and platform has its own instruction
        
        # HAPP
        "install_happ_ios": "Download Happ from the App Store and install the app. After installation, launch it and allow VPN profile creation.",
        "install_happ_android": "Download Happ from Google Play and install the app. After installation, launch it and allow VPN connection creation.",
        "install_happ_windows": "Download Happ from the official website and install the app. After installation, run it as administrator for proper VPN functionality.",
        "install_happ_macos": "Download Happ from the App Store (for M-series) or from the official website (for Intel) and install the app. After installation, launch it and allow VPN profile creation.",
        "install_happ_linux": "Download Happ for Linux from the official website. Install the package with sudo dpkg -i happ.deb command or through your distribution's package manager.",
        "install_happ_appletv": "Install the Happ app on Apple TV through the App Store. Open the app and prepare to add subscription via QR code.",
        "install_happ_androidtv": "Install the Happ app on Android TV through Google Play Store. Open the app and prepare to add subscription via QR code.",
        
        # V2RAYTUN
        "install_v2raytun_ios": "Download v2RayTun from the App Store and install the app. After installation, launch it and allow VPN profile creation.",
        "install_v2raytun_android": "Download v2RayTun from Google Play and install the app. After installation, launch it and allow VPN connection creation.",
        "install_v2raytun_windows": "Download v2RayTun from the official website and install the app. After installation, run it as administrator for proper VPN functionality.",
        "install_v2raytun_macos": "Download v2RayTun from the App Store and install the app. After installation, launch it and allow VPN profile creation.",
        
        # SHADOWROCKET
        "install_shadowrocket_ios": "Download Shadowrocket from the App Store and install the app. After installation, launch it and allow VPN profile creation.",
        "install_shadowrocket_macos": "Download Shadowrocket from the App Store and install the app. After installation, launch it and allow VPN profile creation.",
        
        # STREISAND
        "install_streisand_ios": "Download Streisand from the App Store and install the app. Open App Store. After installation, launch the app and allow VPN profile creation.",
        
        # HIDDIFY
        "install_hiddify_android": "Open Google Play Store, find the HiddifyNG app and install it. After installation, launch the app and allow VPN connection creation.",
        "install_hiddify_windows": "Download Hiddify from the official website and install the app. After installation, run it as administrator for proper VPN functionality.",
        "install_hiddify_macos": "Download Hiddify from the official website and install the app. After installation, launch it and allow VPN profile creation.",
        "install_hiddify_linux": "Download Hiddify for Linux from GitHub. Install the AppImage file or use a package for your distribution.",

        # KOALA CLASH
        "install_koalaclash_macos": "Download Koala Clash from GitHub and install the app. After installation, launch it and allow VPN profile creation.",
        "install_koalaclash_windows": "Download Koala Clash from GitHub and install the app. After installation, run it as administrator for proper VPN functionality.",
        
        # === INSTRUCTIONS FOR ADDING A SUBSCRIPTION ===
        "add_subscription_happ": "Press the button below — the Happ app will open and the subscription will be added automatically.<br><br>If the subscription was not added automatically, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">copy the subscription link</span> and add it to the app manually via the \"<b>+</b>\" button in the upper right corner → \"Paste from clipboard\"",
        "add_subscription_hiddify": "Press the button below — the Hiddify app will open and the subscription will be added automatically.<br><br>If the subscription was not added automatically, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">copy the subscription link</span> and add it to the app manually via the \"<b>+</b>\" button in the upper right corner → \"Add from clipboard\"",
        "add_subscription_v2raytun": "Press the button below — the V2rayTun app will open and the subscription will be added automatically.<br><br>If the subscription was not added automatically, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">copy the subscription link</span> and add it to the app manually via the \"<b>+</b>\" button in the upper right corner → \"Add from buffer\"",
        "add_subscription_shadowrocket": "Press the button below — the Shadowrocket app will open and the subscription will be added automatically.<br><br>If the subscription was not added automatically, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">copy the subscription link</span> and add it to the app manually via the \"<b>+</b>\" button in the upper right corner → \"Save\"",
        "add_subscription_streisand": "Press the button below — the Streisand app will open and the subscription will be added automatically.<br><br>If the subscription was not added automatically, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">copy the subscription link</span> and add it to the app manually via the \"<b>+</b>\" button in the upper right corner → \"Add from buffer\"",
        "add_subscription_koalaclash": "Press the button below — the Koala Clash app will open and the subscription will be added automatically.<br><br>If the subscription was not added automatically, <span class=\"copy-link-text\" onclick=\"window.copyKey()\">copy the subscription link</span> and add it to the app manually via the \"Add profile\" button on the main page → \"Import\"",
        "add_subscription_tv": "Scan the code from TV using the button below. You will need to allow camera access.",
        
        # === INSTRUCTIONS FOR CONNECTING IN APP ===
        # How to enable VPN in each app after adding subscription
        "connect_happ": "In the Happ app, select the required server from the server list and press the large round VPN enable button at the top of the screen.",
        "connect_happ_appletv": "On Apple TV, select the required server from the server list and press the large round VPN enable button.",
        "connect_happ_androidtv": "On Android TV, select the required server from the server list and press the large round VPN enable button.",
        "connect_v2raytun": "In the v2RayTun app, select the required server from the server list and press the VPN enable button at the top of the screen.",
        "connect_shadowrocket": "In the Shadowrocket app, select the required server from the server list and press the toggle in the upper right part of the screen to enable VPN.",
        "connect_streisand": "In the Streisand app, select the required server from the server list and press the VPN enable button at the top of the screen.",
        "connect_hiddify": "In the Hiddify app, press the VPN connection button. You can also select the required server from the \"Profiles\" section.",
        "connect_koalaclash": "In the Koala Clash app, select the required server from the server list and press the VPN enable button to activate the connection.",
        
        # === NOTIFICATIONS ===
        "link_copied": "Link copied!",
        "failed_to_copy": "Failed to copy"
    }
}

