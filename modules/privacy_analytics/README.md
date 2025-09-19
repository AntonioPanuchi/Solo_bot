# Privacy Analytics Module

Модуль для аналитики и мониторинга с соблюдением требований приватности и GDPR.

## Обзор

Модуль `privacy_analytics` предоставляет комплексную систему для:
- Мониторинга серверов и производительности
- Аналитики данных с соблюдением приватности
- Управления согласиями на обработку данных
- Аудита и соответствия требованиям
- Управления хранением данных

## Структура модуля

```
privacy_analytics/
├── __init__.py                 # Основные экспорты модуля
├── router.py                   # FastAPI роутер
├── settings.py                 # Настройки модуля
├── VERSION                     # Версия модуля
├── monitoring/                 # Система мониторинга
│   ├── __init__.py
│   ├── server_monitor.py       # Мониторинг серверов
│   ├── performance_monitor.py  # Мониторинг производительности
│   ├── security_monitor.py     # Мониторинг безопасности
│   └── business_monitor.py     # Мониторинг бизнес-метрик
├── analytics/                  # Система аналитики
│   ├── __init__.py
│   ├── data_processor.py       # Обработка данных
│   ├── metrics_calculator.py   # Расчет метрик
│   └── report_generator.py     # Генерация отчетов
├── dashboards/                 # Дашборды
│   ├── __init__.py
│   ├── realtime_dashboard.py   # Реальное время
│   ├── business_dashboard.py   # Бизнес-метрики
│   └── admin_dashboard.py      # Административный
├── alerts/                     # Система алертов
│   ├── __init__.py
│   ├── alert_manager.py        # Управление алертами
│   ├── notification_channels.py # Каналы уведомлений
│   └── escalation_rules.py     # Правила эскалации
├── api/                        # API модуля
│   ├── __init__.py
│   ├── routes.py               # API маршруты
│   ├── schemas.py              # Pydantic схемы
│   └── middleware.py           # Middleware
├── web/                        # Веб-интерфейс
│   ├── __init__.py
│   ├── app.py                  # Flask приложение
│   ├── templates/              # HTML шаблоны
│   │   ├── dashboard.html
│   │   └── error.html
│   └── static/                 # Статические файлы
│       ├── style.css
│       └── script.js
└── privacy/                    # Система приватности
    ├── __init__.py
    ├── privacy_checker.py      # Проверка приватности
    ├── data_anonymizer.py      # Анонимизация данных
    ├── gdpr_compliance.py      # Соответствие GDPR
    ├── audit_logger.py         # Аудит
    ├── consent_manager.py      # Управление согласиями
    ├── data_retention.py       # Управление хранением
    └── privacy_policy.py       # Политики приватности
```

## Основные компоненты

### 1. Система мониторинга

#### ServerMonitor
- Мониторинг CPU, RAM, диска, сети
- Сбор метрик в реальном времени
- Настраиваемые интервалы

#### PerformanceMonitor
- Мониторинг производительности API
- Отслеживание времени ответа
- Анализ ошибок

#### SecurityMonitor
- Мониторинг безопасности
- Отслеживание неудачных попыток входа
- Выявление подозрительной активности

#### BusinessMonitor
- Бизнес-метрики
- Новые подписки
- Доходы и активные пользователи

### 2. Система аналитики

#### DataProcessor
- Обработка и анонимизация данных
- Агрегация по временным интервалам
- Соблюдение требований приватности

#### MetricsCalculator
- Расчет KPI
- Анализ трендов
- Статистические показатели

#### ReportGenerator
- Генерация отчетов
- Ежедневные, еженедельные, месячные отчеты
- Пользовательские отчеты

### 3. Дашборды

#### RealtimeDashboard
- Метрики в реальном времени
- Системные показатели
- События безопасности

#### BusinessDashboard
- Бизнес-аналитика
- KPI и тренды
- Топ-метрики

#### AdminDashboard
- Административный обзор
- Комбинированные данные
- Система здоровья

### 4. Система алертов

#### AlertManager
- Управление алертами
- Уведомления через различные каналы
- Правила эскалации

#### NotificationChannels
- Telegram
- Email
- Webhooks

#### EscalationRules
- Автоматическая эскалация
- Настраиваемые правила
- Приоритизация

### 5. API

#### RESTful API
- Получение метрик
- Управление алертами
- Генерация отчетов
- Аутентификация по API ключу

#### Схемы данных
- Pydantic модели
- Валидация данных
- Документация API

### 6. Веб-интерфейс

#### Flask приложение
- Интерактивные дашборды
- Управление настройками
- Просмотр алертов

#### Шаблоны
- Responsive дизайн
- Chart.js для графиков
- Современный UI

### 7. Система приватности

#### PrivacyChecker
- Проверка соответствия политикам
- Валидация данных
- Мониторинг нарушений

#### DataAnonymizer
- Анонимизация данных
- Псевдонимизация
- Хеширование

#### GDPRCompliance
- Соответствие GDPR
- Права субъектов данных
- Уведомления о нарушениях

#### AuditLogger
- Логирование аудита
- Отслеживание действий
- Целостность данных

#### ConsentManager
- Управление согласиями
- Отзыв согласий
- История изменений

#### DataRetentionManager
- Управление хранением
- Политики хранения
- Автоматическое удаление

#### PrivacyPolicyManager
- Управление политиками
- Версионирование
- Соответствие требованиям

## Настройки

### Основные настройки

```python
# Включение/отключение модуля
ENABLED: bool = True

# Уровень логирования
LOG_LEVEL: str = "INFO"

# Период хранения данных (дни)
DATA_RETENTION_DAYS: int = 365

# Интервалы мониторинга (секунды)
SERVER_MONITOR_INTERVAL_SECONDS: int = 60
PERFORMANCE_MONITOR_INTERVAL_SECONDS: int = 30
SECURITY_MONITOR_INTERVAL_SECONDS: int = 300
BUSINESS_MONITOR_INTERVAL_SECONDS: int = 3600

# Настройки анонимизации
ANONYMIZATION_LEVEL: str = "full"  # "full", "partial", "none"
AGGREGATION_INTERVAL_SECONDS: int = 3600

# Пороги алертов
ALERT_THRESHOLD_CPU_USAGE: float = 80.0
ALERT_THRESHOLD_RAM_USAGE: float = 85.0
ALERT_THRESHOLD_DISK_USAGE: float = 90.0
ALERT_THRESHOLD_FAILED_LOGINS: int = 5

# API настройки
API_PREFIX: str = "/privacy-analytics"
API_KEY: str = "supersecretapikey"

# Веб-интерфейс
WEB_ENABLED: bool = True
WEB_PATH_PREFIX: str = "/admin/privacy-analytics"
WEB_SECRET_KEY: str = "another_super_secret_key"
```

### Настройки приватности

```python
# Уровни анонимизации
ANONYMIZATION_LEVEL: str = "full"

# Период хранения аудита
AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 лет

# Настройки согласий
CONSENT_REQUIRED: bool = True
CONSENT_EXPIRY_DAYS: int = 365

# Настройки хранения
DATA_RETENTION_POLICY: str = "standard"
AUTO_DELETE_EXPIRED: bool = True
```

## Использование

### 1. Инициализация модуля

```python
from modules.privacy_analytics import router, settings

# Модуль автоматически загружается в main.py
```

### 2. Мониторинг

```python
from modules.privacy_analytics.monitoring import ServerMonitor

monitor = ServerMonitor()
await monitor.start_monitoring()
```

### 3. Аналитика

```python
from modules.privacy_analytics.analytics import DataProcessor

processor = DataProcessor()
await processor.process_raw_log(log_entry)
```

### 4. Алерты

```python
from modules.privacy_analytics.alerts import AlertManager

alert_manager = AlertManager()
await alert_manager.trigger_alert("server_cpu_high", "warning", "CPU usage is high")
```

### 5. Управление согласиями

```python
from modules.privacy_analytics.privacy import ConsentManager, ConsentPurpose

consent_manager = ConsentManager()
await consent_manager.create_consent("user123", ConsentPurpose.ANALYTICS)
```

### 6. API

```bash
# Получение метрик сервера
curl -H "X-API-Key: supersecretapikey" \
     http://localhost:8000/privacy-analytics/metrics/server

# Получение KPI
curl -H "X-API-Key: supersecretapikey" \
     http://localhost:8000/privacy-analytics/analytics/kpis
```

## Безопасность и приватность

### Анонимизация данных
- Хеширование идентификаторов
- Псевдонимизация
- Удаление PII

### Шифрование
- Шифрование чувствительных данных
- Безопасное хранение ключей
- Передача по HTTPS

### Аудит
- Логирование всех действий
- Отслеживание доступа к данным
- Мониторинг нарушений

### Соответствие GDPR
- Права субъектов данных
- Управление согласиями
- Уведомления о нарушениях
- Политики хранения

## Мониторинг и алерты

### Метрики
- Производительность системы
- Использование ресурсов
- Бизнес-показатели
- События безопасности

### Алерты
- Автоматические уведомления
- Множественные каналы
- Эскалация по правилам
- Настраиваемые пороги

### Дашборды
- Реальное время
- Исторические данные
- Интерактивные графики
- Экспорт данных

## Развертывание

### Требования
- Python 3.8+
- FastAPI
- Flask
- SQLAlchemy
- psutil
- httpx

### Установка
1. Модуль автоматически загружается в SoloBot
2. Настройте переменные окружения
3. Запустите бота

### Конфигурация
1. Отредактируйте `settings.py`
2. Настройте каналы уведомлений
3. Настройте политики приватности

## Поддержка

### Логирование
- Структурированные логи
- Различные уровни
- Ротация логов

### Мониторинг
- Health checks
- Метрики производительности
- Алерты

### Документация
- API документация
- Примеры использования
- Руководства по настройке

## Лицензия

Модуль является частью проекта SoloBot и распространяется под той же лицензией.

## Версия

Текущая версия: 0.1.0

## Автор

SoloBot Development Team
