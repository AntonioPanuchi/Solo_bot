"""
Настройки модуля Privacy-Compliant Analytics & Monitoring
"""

# ========================================
# 🔧 ОСНОВНЫЕ НАСТРОЙКИ
# ========================================

# Включение/выключение модуля
ANALYTICS_ENABLED = True
MONITORING_ENABLED = True
DASHBOARD_ENABLED = True
ALERTS_ENABLED = True

# Уровни логирования
LOG_LEVEL = "INFO"
AUDIT_LOG_LEVEL = "AUDIT"
PERFORMANCE_LOG_LEVEL = "PERF"

# ========================================
# 🔒 НАСТРОЙКИ ПРИВАТНОСТИ
# ========================================

# Режим приватности: strict, balanced, minimal
PRIVACY_MODE = "strict"

# Анонимизация данных
DATA_ANONYMIZATION = True
PERSONAL_DATA_FILTERING = True
AUDIT_PRIVACY_COMPLIANCE = True

# Запрещенные паттерны данных
FORBIDDEN_DATA_PATTERNS = [
    "user_id",
    "ip_address", 
    "personal_data",
    "browsing_history",
    "website_visit",
    "domain_name",
    "individual_connection",
    "user_agent"
]

# ========================================
# 💾 ХРАНЕНИЕ ДАННЫХ
# ========================================

# Срок хранения данных (дни)
DATA_RETENTION_DAYS = 90
REAL_TIME_DATA_HOURS = 24

# Архивирование
ARCHIVE_OLD_DATA = True
COMPRESS_ARCHIVES = True

# ========================================
# 📊 МОНИТОРИНГ
# ========================================

# Интервалы сбора данных (секунды)
SERVER_MONITORING_INTERVAL = 30
PERFORMANCE_METRICS_INTERVAL = 60
HEALTH_CHECK_INTERVAL = 300
SECURITY_MONITORING_INTERVAL = 120

# ========================================
# 🚨 ПОРОГОВЫЕ ЗНАЧЕНИЯ ДЛЯ АЛЕРТОВ
# ========================================

ALERT_THRESHOLDS = {
    # Системные метрики
    "server_cpu_usage": 80,  # %
    "server_memory_usage": 85,  # %
    "server_disk_usage": 90,  # %
    "connection_latency": 500,  # мс
    "error_rate": 5,  # %
    
    # Бизнес-метрики
    "failed_payments": 10,  # в час
    "unusual_traffic_spike": 200,  # % от нормы
    "low_conversion_rate": 2,  # %
    
    # Безопасность
    "failed_login_attempts": 10,  # в час
    "suspicious_activity": 5,  # событий в час
    "privilege_escalation_attempts": 3,  # в день
}

# ========================================
# 📡 ИНТЕГРАЦИИ
# ========================================

# Внешние системы мониторинга
PROMETHEUS_ENABLED = True
GRAFANA_ENABLED = True
ELASTICSEARCH_ENABLED = True

# Каналы уведомлений
TELEGRAM_ALERTS_ENABLED = True
EMAIL_ALERTS_ENABLED = True
WEBHOOK_ALERTS_ENABLED = True

# Настройки Telegram уведомлений
TELEGRAM_ALERT_CHAT_ID = ""  # ID чата для алертов
TELEGRAM_ALERT_BOT_TOKEN = ""  # Токен бота для алертов

# Настройки Email уведомлений
EMAIL_ALERT_SMTP_SERVER = ""
EMAIL_ALERT_SMTP_PORT = 587
EMAIL_ALERT_USERNAME = ""
EMAIL_ALERT_PASSWORD = ""
EMAIL_ALERT_FROM = ""
EMAIL_ALERT_TO = []

# ========================================
# 🎛️ ДАШБОРДЫ
# ========================================

# Интервалы обновления (секунды)
DASHBOARD_REFRESH_INTERVAL = 30
REAL_TIME_UPDATE_INTERVAL = 5
HISTORICAL_DATA_DAYS = 30

# Настройки веб-интерфейса
DASHBOARD_PORT = 3024
DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_BASE_PATH = "/analytics/"

# ========================================
# 🔌 API НАСТРОЙКИ
# ========================================

# Ограничения API
API_RATE_LIMIT = 1000  # запросов в час
API_AUTHENTICATION = True
API_DOCUMENTATION = True

# CORS настройки
API_CORS_ORIGINS = ["*"]
API_CORS_METHODS = ["GET", "POST", "PUT", "DELETE"]
API_CORS_HEADERS = ["*"]

# ========================================
# 📈 АНАЛИТИКА
# ========================================

# Настройки агрегации данных
AGGREGATION_INTERVALS = {
    "realtime": 60,  # секунды
    "hourly": 3600,  # секунды
    "daily": 86400,  # секунды
    "weekly": 604800,  # секунды
}

# Метрики для отслеживания
TRACKED_METRICS = [
    "server_performance",
    "connection_quality",
    "business_metrics",
    "security_events",
    "system_health"
]

# ========================================
# 🔍 ПОИСК И ФИЛЬТРАЦИЯ
# ========================================

# Настройки поиска
SEARCH_ENGINE = "sqlite"  # sqlite, postgresql, elasticsearch
SEARCH_INDEX_PREFIX = "privacy_analytics"
SEARCH_RESULTS_LIMIT = 1000

# ========================================
# 📊 ОТЧЕТЫ
# ========================================

# Автоматические отчеты
AUTO_REPORTS_ENABLED = True
DAILY_REPORT_TIME = "09:00"  # Время отправки ежедневного отчета
WEEKLY_REPORT_DAY = "monday"  # День недели для еженедельного отчета
MONTHLY_REPORT_DAY = 1  # День месяца для ежемесячного отчета

# Форматы отчетов
REPORT_FORMATS = ["json", "csv", "html"]
REPORT_EMAIL_TEMPLATE = "analytics_report.html"

# ========================================
# 🛡️ БЕЗОПАСНОСТЬ
# ========================================

# Настройки безопасности
ENCRYPT_SENSITIVE_DATA = True
AUDIT_LOG_RETENTION_DAYS = 365
SECURITY_EVENT_RETENTION_DAYS = 180

# IP-адреса для доступа к дашборду (пустой список = доступ для всех)
DASHBOARD_ALLOWED_IPS = []

# ========================================
# 🌍 ГЕОГРАФИЧЕСКИЕ НАСТРОЙКИ
# ========================================

# Часовой пояс для отображения времени
TIMEZONE = "Europe/Moscow"

# Язык интерфейса
DEFAULT_LANGUAGE = "ru"

# ========================================
# 🔧 РАСШИРЕННЫЕ НАСТРОЙКИ
# ========================================

# Настройки производительности
MAX_CONCURRENT_MONITORING_TASKS = 10
METRICS_BATCH_SIZE = 100
CACHE_TTL_SECONDS = 300

# Настройки логирования
LOG_ROTATION_SIZE = "100MB"
LOG_ROTATION_COUNT = 5
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Настройки базы данных
DB_CONNECTION_POOL_SIZE = 10
DB_CONNECTION_TIMEOUT = 30
DB_QUERY_TIMEOUT = 60
