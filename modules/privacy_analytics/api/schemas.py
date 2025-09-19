"""
Схемы данных для API Privacy-Compliant Analytics
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


# ========================================
# 📊 ОСНОВНЫЕ СХЕМЫ
# ========================================

class HealthResponse(BaseModel):
    """Ответ проверки здоровья"""
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]


class ErrorResponse(BaseModel):
    """Ответ об ошибке"""
    error: str
    message: str
    timestamp: str
    request_id: Optional[str] = None


# ========================================
# 📊 МОНИТОРИНГ
# ========================================

class ServerStatusResponse(BaseModel):
    """Ответ статуса сервера"""
    server_id: str
    status: str
    health_score: float
    last_update: str
    active_connections: int
    bandwidth_usage_gb: float
    cpu_usage: float
    memory_usage: float


class PerformanceMetricsResponse(BaseModel):
    """Ответ метрик производительности"""
    status: str
    last_update: str
    response_time_ms: float
    rps: float
    error_rate: float
    health_score: float
    active_users: int


class SecurityMetricsResponse(BaseModel):
    """Ответ метрик безопасности"""
    threat_level: str
    failed_logins: int
    suspicious_ips: int
    brute_force_active: bool
    last_check: str


class BusinessMetricsResponse(BaseModel):
    """Ответ бизнес-метрик"""
    status: str
    last_update: str
    total_users: int
    active_users: int
    daily_revenue: float
    monthly_revenue: float
    conversion_rate: float
    retention_rate: float


# ========================================
# 📈 АНАЛИТИКА
# ========================================

class MetricsProcessingRequest(BaseModel):
    """Запрос обработки метрик"""
    server_id: str
    timestamp: str
    metrics: Dict[str, Any]
    privacy_compliant: bool = True


class ProcessingResponse(BaseModel):
    """Ответ обработки метрик"""
    success: bool
    processed_metrics: Dict[str, Any]
    timestamp: str


class PerformanceAnalysisResponse(BaseModel):
    """Ответ анализа производительности"""
    performance_score: float
    efficiency_metrics: Dict[str, float]
    bottlenecks: List[str]
    recommendations: List[str]


class BusinessAnalysisResponse(BaseModel):
    """Ответ бизнес-анализа"""
    revenue_metrics: Dict[str, float]
    user_metrics: Dict[str, Any]
    conversion_metrics: Dict[str, float]


# ========================================
# 📊 ДАШБОРДЫ
# ========================================

class RealtimeDashboardResponse(BaseModel):
    """Ответ дашборда в реальном времени"""
    timestamp: str
    current_metrics: Dict[str, Any]
    server_status: Dict[str, Any]
    alerts: Dict[str, Any]
    performance_graphs: Dict[str, Any]
    privacy_status: str


class BusinessDashboardResponse(BaseModel):
    """Ответ бизнес-дашборда"""
    timestamp: str
    revenue_metrics: Dict[str, Any]
    user_metrics: Dict[str, Any]
    subscription_metrics: Dict[str, Any]
    geographic_metrics: Dict[str, Any]
    conversion_metrics: Dict[str, Any]
    privacy_status: str


class AdminDashboardResponse(BaseModel):
    """Ответ административного дашборда"""
    timestamp: str
    system_overview: Dict[str, Any]
    server_management: Dict[str, Any]
    user_management: Dict[str, Any]
    security_overview: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    alerts_summary: Dict[str, Any]
    privacy_status: str


# ========================================
# 🚨 АЛЕРТЫ
# ========================================

class AlertSeverity(str, Enum):
    """Серьезность алерта"""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class AlertStatus(str, Enum):
    """Статус алерта"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class AlertResponse(BaseModel):
    """Ответ алерта"""
    id: str
    rule_id: str
    rule_name: str
    severity: AlertSeverity
    message: str
    timestamp: str
    status: AlertStatus
    escalation_level: int
    acknowledged: bool
    resolved: bool


class AcknowledgeRequest(BaseModel):
    """Запрос подтверждения алерта"""
    acknowledged_by: str


class AcknowledgeResponse(BaseModel):
    """Ответ подтверждения алерта"""
    success: bool
    message: str


class ResolveRequest(BaseModel):
    """Запрос разрешения алерта"""
    resolved_by: str


class ResolveResponse(BaseModel):
    """Ответ разрешения алерта"""
    success: bool
    message: str


class AlertStatisticsResponse(BaseModel):
    """Ответ статистики алертов"""
    active_alerts: int
    total_alerts: int
    alerts_24h: int
    severity_distribution: Dict[str, int]
    resolution_rate: float
    avg_resolution_time_minutes: float


# ========================================
# 📄 ОТЧЕТЫ
# ========================================

class ReportType(str, Enum):
    """Тип отчета"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class ReportResponse(BaseModel):
    """Ответ отчета"""
    id: str
    name: str
    description: str
    sections: List[str]
    last_generated: Optional[str] = None


class ReportGenerationRequest(BaseModel):
    """Запрос генерации отчета"""
    report_type: ReportType
    parameters: Optional[Dict[str, Any]] = None


class ReportGenerationResponse(BaseModel):
    """Ответ генерации отчета"""
    success: bool
    report: Dict[str, Any]
    generated_at: str


# ========================================
# 🔒 ПРИВАТНОСТЬ
# ========================================

class PrivacyComplianceResponse(BaseModel):
    """Ответ соответствия приватности"""
    compliant: bool
    last_check: str
    privacy_mode: str
    data_anonymization: bool
    personal_data_filtering: bool


# ========================================
# 📊 СТАТИСТИКА
# ========================================

class StatisticsOverviewResponse(BaseModel):
    """Ответ обзора статистики"""
    total_requests: int
    success_rate: float
    average_response_time: float
    active_users: int
    system_uptime: float
    last_updated: str


# ========================================
# 🔧 УПРАВЛЕНИЕ
# ========================================

class RefreshResponse(BaseModel):
    """Ответ обновления данных"""
    success: bool
    message: str
    timestamp: str


class ConfigResponse(BaseModel):
    """Ответ конфигурации"""
    privacy_mode: str
    monitoring_enabled: bool
    alerts_enabled: bool
    dashboard_enabled: bool
    data_retention_days: int
    real_time_update_interval: int
    dashboard_refresh_interval: int


# ========================================
# 📚 ДОКУМЕНТАЦИЯ
# ========================================

class ApiDocumentationResponse(BaseModel):
    """Ответ документации API"""
    title: str
    version: str
    description: str
    endpoints: List[Dict[str, str]]
    privacy_compliance: str
    rate_limits: Dict[str, int]


# ========================================
# 🔄 ВЕБХУКИ
# ========================================

class WebhookRequest(BaseModel):
    """Запрос вебхука"""
    type: str
    data: Dict[str, Any]
    timestamp: str
    signature: Optional[str] = None


class WebhookResponse(BaseModel):
    """Ответ вебхука"""
    status: str
    message: Optional[str] = None
    processed_at: str


# ========================================
# 📊 МЕТРИКИ И АНАЛИТИКА
# ========================================

class MetricDataPoint(BaseModel):
    """Точка данных метрики"""
    timestamp: str
    value: float
    tags: Optional[Dict[str, str]] = None


class MetricSeries(BaseModel):
    """Серия метрик"""
    name: str
    data_points: List[MetricDataPoint]
    unit: Optional[str] = None


class AnalyticsQuery(BaseModel):
    """Запрос аналитики"""
    metric_names: List[str]
    start_time: str
    end_time: str
    aggregation: Optional[str] = "avg"
    group_by: Optional[List[str]] = None


class AnalyticsResponse(BaseModel):
    """Ответ аналитики"""
    query: AnalyticsQuery
    results: List[MetricSeries]
    total_points: int
    execution_time_ms: float


# ========================================
# 🎯 ФИЛЬТРЫ И ПОИСК
# ========================================

class FilterCriteria(BaseModel):
    """Критерии фильтрации"""
    field: str
    operator: str  # eq, ne, gt, lt, gte, lte, in, not_in, contains
    value: Any


class SearchRequest(BaseModel):
    """Запрос поиска"""
    query: str
    filters: Optional[List[FilterCriteria]] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"
    limit: Optional[int] = 100
    offset: Optional[int] = 0


class SearchResponse(BaseModel):
    """Ответ поиска"""
    results: List[Dict[str, Any]]
    total: int
    limit: int
    offset: int
    query_time_ms: float


# ========================================
# 🔔 УВЕДОМЛЕНИЯ
# ========================================

class NotificationChannel(str, Enum):
    """Канал уведомлений"""
    TELEGRAM = "telegram"
    EMAIL = "email"
    WEBHOOK = "webhook"
    SMS = "sms"


class NotificationRequest(BaseModel):
    """Запрос уведомления"""
    channels: List[NotificationChannel]
    message: str
    severity: AlertSeverity
    recipients: Optional[List[str]] = None


class NotificationResponse(BaseModel):
    """Ответ уведомления"""
    success: bool
    sent_channels: List[str]
    failed_channels: List[str]
    message_id: Optional[str] = None


# ========================================
# 📈 ПРОГНОЗЫ И ПРЕДСКАЗАНИЯ
# ========================================

class ForecastRequest(BaseModel):
    """Запрос прогноза"""
    metric_name: str
    forecast_hours: int
    confidence_level: float = 0.95


class ForecastResponse(BaseModel):
    """Ответ прогноза"""
    metric_name: str
    forecast_data: List[MetricDataPoint]
    confidence_intervals: List[Dict[str, float]]
    accuracy_score: float
    generated_at: str


# ========================================
# 🔐 АУТЕНТИФИКАЦИЯ И АВТОРИЗАЦИЯ
# ========================================

class AuthToken(BaseModel):
    """Токен аутентификации"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    scope: Optional[List[str]] = None


class AuthRequest(BaseModel):
    """Запрос аутентификации"""
    username: str
    password: str
    client_id: Optional[str] = None


class AuthResponse(BaseModel):
    """Ответ аутентификации"""
    success: bool
    token: Optional[AuthToken] = None
    user_info: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


# ========================================
# 📊 ЭКСПОРТ И ИМПОРТ
# ========================================

class ExportRequest(BaseModel):
    """Запрос экспорта"""
    data_type: str
    format: str  # json, csv, xlsx, pdf
    filters: Optional[List[FilterCriteria]] = None
    date_range: Optional[Dict[str, str]] = None


class ExportResponse(BaseModel):
    """Ответ экспорта"""
    success: bool
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    expires_at: Optional[str] = None
    download_token: Optional[str] = None


# ========================================
# 🔧 СИСТЕМНЫЕ ОПЕРАЦИИ
# ========================================

class SystemOperationRequest(BaseModel):
    """Запрос системной операции"""
    operation: str  # restart, backup, maintenance, update
    parameters: Optional[Dict[str, Any]] = None
    scheduled_time: Optional[str] = None


class SystemOperationResponse(BaseModel):
    """Ответ системной операции"""
    success: bool
    operation_id: str
    status: str
    message: str
    estimated_duration_minutes: Optional[int] = None
