# Установка и настройка модуля Privacy Analytics

## Требования

### Системные требования
- Python 3.8 или выше
- Операционная система: Linux, macOS, Windows
- Минимум 2 GB RAM
- 1 GB свободного места на диске

### Зависимости
- SoloBot (основной проект)
- FastAPI
- Flask
- SQLAlchemy
- psutil
- httpx
- pandas
- numpy
- cryptography
- faker
- python-telegram-bot
- redis (опционально)

## Установка

### 1. Автоматическая установка

Модуль автоматически загружается в SoloBot при запуске. Никаких дополнительных действий не требуется.

### 2. Автоматическая установка зависимостей

Модуль автоматически устанавливает зависимости при загрузке. Никаких дополнительных действий не требуется.

#### Ручная установка (если нужна)

```bash
# Использование встроенного скрипта
python modules/privacy_analytics/install_deps.py

# Или через менеджер зависимостей
python -m modules.privacy_analytics.dependency_manager --install --verbose

# Или традиционный способ
pip install -r modules/privacy_analytics/requirements.txt
```

#### Управление зависимостями

```bash
# Проверка зависимостей
python -m modules.privacy_analytics.dependency_manager --check --verbose

# Создание lock файла
python -m modules.privacy_analytics.dependency_manager --lock

# Установка из lock файла
python -m modules.privacy_analytics.dependency_manager --install-lock

# Очистка кэша
python -m modules.privacy_analytics.dependency_manager --cleanup
```

### 3. Установка с Docker

```dockerfile
# Добавьте в Dockerfile SoloBot
COPY modules/privacy_analytics/ /app/modules/privacy_analytics/
RUN pip install -r modules/privacy_analytics/requirements.txt
```

## Настройка

### 1. Переменные окружения

Создайте файл `.env` или добавьте переменные в существующий:

```env
# Основные настройки
PRIVACY_ANALYTICS_ENABLED=true
PRIVACY_ANALYTICS_LOG_LEVEL=INFO
PRIVACY_ANALYTICS_DATA_RETENTION_DAYS=365

# API настройки
PRIVACY_ANALYTICS_API_KEY=your_super_secret_api_key
PRIVACY_ANALYTICS_API_PREFIX=/privacy-analytics

# Веб-интерфейс
PRIVACY_ANALYTICS_WEB_ENABLED=true
PRIVACY_ANALYTICS_WEB_PATH_PREFIX=/admin/privacy-analytics
PRIVACY_ANALYTICS_WEB_SECRET_KEY=your_web_secret_key

# Мониторинг
PRIVACY_ANALYTICS_SERVER_MONITOR_INTERVAL_SECONDS=60
PRIVACY_ANALYTICS_PERFORMANCE_MONITOR_INTERVAL_SECONDS=30
PRIVACY_ANALYTICS_SECURITY_MONITOR_INTERVAL_SECONDS=300
PRIVACY_ANALYTICS_BUSINESS_MONITOR_INTERVAL_SECONDS=3600

# Алерты
PRIVACY_ANALYTICS_ALERT_NOTIFICATION_CHANNELS=telegram,email
PRIVACY_ANALYTICS_ALERT_THRESHOLD_CPU_USAGE=80.0
PRIVACY_ANALYTICS_ALERT_THRESHOLD_RAM_USAGE=85.0
PRIVACY_ANALYTICS_ALERT_THRESHOLD_DISK_USAGE=90.0
PRIVACY_ANALYTICS_ALERT_THRESHOLD_FAILED_LOGINS=5

# Приватность
PRIVACY_ANALYTICS_ANONYMIZATION_LEVEL=full
PRIVACY_ANALYTICS_AGGREGATION_INTERVAL_SECONDS=3600
PRIVACY_ANALYTICS_AUDIT_LOG_RETENTION_DAYS=2555

# Telegram (для алертов)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Email (для алертов)
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USER=alerts@example.com
SMTP_PASSWORD=your_smtp_password
SMTP_SENDER_EMAIL=alerts@example.com
SMTP_RECIPIENT_EMAILS=admin@example.com,security@example.com

# База данных (если используется отдельная)
PRIVACY_ANALYTICS_DATABASE_URL=sqlite:///./privacy_analytics.db
```

### 2. Конфигурационный файл

Скопируйте и отредактируйте `config.yaml`:

```bash
cp modules/privacy_analytics/config.yaml.example modules/privacy_analytics/config.yaml
```

Отредактируйте настройки в соответствии с вашими требованиями.

### 3. Настройка базы данных

#### SQLite (по умолчанию)
Никаких дополнительных действий не требуется. База данных создается автоматически.

#### PostgreSQL
```env
PRIVACY_ANALYTICS_DATABASE_URL=postgresql://user:password@localhost:5432/privacy_analytics
```

#### MySQL
```env
PRIVACY_ANALYTICS_DATABASE_URL=mysql://user:password@localhost:3306/privacy_analytics
```

### 4. Настройка Redis (опционально)

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_redis_password
```

## Первоначальная настройка

### 1. Запуск модуля

```bash
# Запуск SoloBot (модуль загрузится автоматически)
python main.py

# Или запуск только модуля для тестирования
python -m modules.privacy_analytics.examples
```

### 2. Проверка работоспособности

```bash
# Проверка API
curl -H "X-API-Key: your_super_secret_api_key" \
     http://localhost:8000/privacy-analytics/health

# Проверка веб-интерфейса
open http://localhost:8000/admin/privacy-analytics
```

### 3. Настройка алертов

#### Telegram
1. Создайте бота через @BotFather
2. Получите токен бота
3. Добавьте токен в переменные окружения
4. Получите chat_id для уведомлений

#### Email
1. Настройте SMTP сервер
2. Добавьте учетные данные в переменные окружения
3. Укажите получателей уведомлений

### 4. Настройка политик приватности

1. Откройте веб-интерфейс
2. Перейдите в раздел "Privacy Policies"
3. Настройте политики в соответствии с вашими требованиями
4. Установите уровни анонимизации

## Проверка установки

### 1. Тесты

```bash
# Запуск всех тестов
python -m pytest modules/privacy_analytics/tests.py -v

# Запуск конкретного теста
python -m pytest modules/privacy_analytics/tests.py::TestServerMonitor -v
```

### 2. Примеры использования

```bash
# Запуск примеров
python modules/privacy_analytics/examples.py
```

### 3. Мониторинг

```bash
# Проверка метрик
curl -H "X-API-Key: your_super_secret_api_key" \
     http://localhost:8000/privacy-analytics/metrics/server

# Проверка алертов
curl -H "X-API-Key: your_super_secret_api_key" \
     http://localhost:8000/privacy-analytics/alerts/active
```

## Устранение неполадок

### 1. Модуль не загружается

**Проблема**: Модуль не появляется в списке загруженных модулей.

**Решение**:
- Проверьте, что файл `modules/privacy_analytics/__init__.py` существует
- Убедитесь, что все зависимости установлены
- Проверьте логи на наличие ошибок

### 2. Ошибки базы данных

**Проблема**: Ошибки при работе с базой данных.

**Решение**:
- Проверьте URL базы данных
- Убедитесь, что база данных доступна
- Проверьте права доступа

### 3. Алерты не отправляются

**Проблема**: Алерты не приходят в Telegram или Email.

**Решение**:
- Проверьте настройки каналов уведомлений
- Убедитесь, что токены и пароли корректны
- Проверьте сетевое подключение

### 4. Высокое потребление ресурсов

**Проблема**: Модуль потребляет много CPU или памяти.

**Решение**:
- Увеличьте интервалы мониторинга
- Отключите ненужные компоненты
- Настройте агрегацию данных

### 5. Ошибки приватности

**Проблема**: Нарушения политик приватности.

**Решение**:
- Проверьте настройки анонимизации
- Убедитесь, что согласия получены
- Настройте политики хранения данных

## Обновление

### 1. Обновление модуля

```bash
# Остановите SoloBot
# Обновите файлы модуля
# Перезапустите SoloBot
```

### 2. Миграция базы данных

```bash
# Создание миграции
alembic revision --autogenerate -m "Update privacy analytics"

# Применение миграции
alembic upgrade head
```

### 3. Обновление конфигурации

1. Сравните старую и новую конфигурацию
2. Обновите настройки
3. Перезапустите модуль

## Удаление

### 1. Остановка модуля

```bash
# Остановите SoloBot
# Модуль будет автоматически отключен
```

### 2. Удаление данных

```bash
# Удаление базы данных (если используется отдельная)
rm privacy_analytics.db

# Удаление логов
rm -rf logs/privacy_analytics/
```

### 3. Удаление зависимостей

```bash
# Удаление пакетов (осторожно!)
pip uninstall -r modules/privacy_analytics/requirements.txt
```

## Поддержка

### 1. Логи

```bash
# Просмотр логов
tail -f logs/privacy_analytics.log

# Логи с фильтрацией
grep "ERROR" logs/privacy_analytics.log
```

### 2. Мониторинг

```bash
# Проверка статуса
curl -H "X-API-Key: your_super_secret_api_key" \
     http://localhost:8000/privacy-analytics/status

# Проверка здоровья
curl -H "X-API-Key: your_super_secret_api_key" \
     http://localhost:8000/privacy-analytics/health
```

### 3. Документация

- README.md - Основная документация
- examples.py - Примеры использования
- tests.py - Тесты
- config.yaml - Конфигурация

### 4. Сообщество

- GitHub Issues - Сообщения об ошибках
- Discord - Обсуждения
- Telegram - Поддержка

## Безопасность

### 1. API ключи

- Используйте сильные API ключи
- Регулярно меняйте ключи
- Не храните ключи в коде

### 2. База данных

- Используйте шифрование
- Регулярно делайте резервные копии
- Ограничьте доступ

### 3. Сеть

- Используйте HTTPS
- Настройте файрвол
- Ограничьте доступ к API

### 4. Логи

- Не логируйте чувствительные данные
- Регулярно ротируйте логи
- Ограничьте доступ к логам

## Производительность

### 1. Оптимизация

- Настройте агрегацию данных
- Используйте кэширование
- Оптимизируйте запросы к БД

### 2. Масштабирование

- Используйте Redis для кэширования
- Настройте горизонтальное масштабирование
- Используйте балансировщик нагрузки

### 3. Мониторинг

- Отслеживайте производительность
- Настройте алерты
- Регулярно анализируйте метрики
