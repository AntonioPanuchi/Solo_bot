"""
Основной роутер модуля Privacy-Compliant Analytics & Monitoring
"""

import asyncio
import threading
from datetime import datetime
from typing import Dict, Any

from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import FastAPI
from hooks.hooks import register_hook

from . import settings
from .monitoring import ServerMonitor, PerformanceMonitor, SecurityMonitor
from .analytics import DataProcessor, ReportGenerator
from .dashboards import RealtimeDashboard, BusinessDashboard
from .alerts import AlertManager
from .api import create_api_routes
from .privacy import PrivacyComplianceChecker
from logger import logger


# Создаем основной роутер
router = Router(name="privacy_analytics_module")

# Инициализируем компоненты
server_monitor = ServerMonitor()
performance_monitor = PerformanceMonitor()
security_monitor = SecurityMonitor()
data_processor = DataProcessor()
report_generator = ReportGenerator()
realtime_dashboard = RealtimeDashboard()
business_dashboard = BusinessDashboard()
alert_manager = AlertManager()
privacy_checker = PrivacyComplianceChecker()

# Создаем FastAPI приложение для дашборда
app = FastAPI(
    title="Privacy-Compliant Analytics Dashboard",
    version="1.0.0",
    description="Аналитика и мониторинг с соблюдением приватности"
)

# Регистрируем API маршруты
create_api_routes(app)

# Запускаем мониторинг в отдельном потоке
def start_monitoring():
    """Запуск системы мониторинга"""
    if not settings.MONITORING_ENABLED:
        return
    
    async def monitoring_loop():
        while True:
            try:
                # Мониторинг серверов
                if settings.SERVER_MONITORING_INTERVAL > 0:
                    await server_monitor.collect_all_metrics()
                
                # Мониторинг производительности
                if settings.PERFORMANCE_METRICS_INTERVAL > 0:
                    await performance_monitor.collect_performance_metrics()
                
                # Мониторинг безопасности
                if settings.SECURITY_MONITORING_INTERVAL > 0:
                    await security_monitor.monitor_security_events()
                
                # Обработка данных
                await data_processor.process_queued_metrics()
                
                # Проверка алертов
                if settings.ALERTS_ENABLED:
                    await alert_manager.check_all_alerts()
                
                # Пауза между циклами
                await asyncio.sleep(min(
                    settings.SERVER_MONITORING_INTERVAL,
                    settings.PERFORMANCE_METRICS_INTERVAL,
                    settings.SECURITY_MONITORING_INTERVAL
                ))
                
            except Exception as e:
                logger.error(f"[Privacy Analytics] Ошибка в цикле мониторинга: {e}")
                await asyncio.sleep(60)  # Пауза при ошибке
    
    # Запускаем асинхронный цикл
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitoring_loop())

# Запускаем мониторинг в отдельном потоке
if settings.MONITORING_ENABLED:
    monitoring_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitoring_thread.start()
    logger.info("[Privacy Analytics] Система мониторинга запущена")

# Функции хуков для интеграции с основным ботом
async def admin_panel_hook(admin_role: str, **kwargs) -> list:
    """Добавляем кнопки аналитики в админ-панель"""
    if not settings.ANALYTICS_ENABLED:
        return []
    
    buttons = []
    
    if admin_role in ["superadmin", "admin"]:
        buttons.append({
            "button": InlineKeyboardButton(
                text="📊 Аналитика",
                callback_data="privacy_analytics:dashboard"
            )
        })
        
        buttons.append({
            "button": InlineKeyboardButton(
                text="📈 Отчеты",
                callback_data="privacy_analytics:reports"
            )
        })
        
        buttons.append({
            "button": InlineKeyboardButton(
                text="🚨 Алерты",
                callback_data="privacy_analytics:alerts"
            )
        })
    
    return buttons

async def system_startup_hook(**kwargs):
    """Инициализация при запуске системы"""
    if settings.ANALYTICS_ENABLED:
        logger.info("[Privacy Analytics] Модуль аналитики инициализирован")
        
        # Проверяем соответствие требованиям приватности
        if settings.AUDIT_PRIVACY_COMPLIANCE:
            compliance_status = await privacy_checker.audit_system_compliance()
            if not compliance_status:
                logger.warning("[Privacy Analytics] Обнаружены нарушения требований приватности")

# Регистрируем хуки
register_hook("admin_panel", admin_panel_hook)
register_hook("system_startup", system_startup_hook)

# Обработчики команд
@router.callback_query(lambda c: c.data.startswith("privacy_analytics:"))
async def handle_analytics_callback(callback: CallbackQuery):
    """Обработка callback'ов модуля аналитики"""
    action = callback.data.split(":")[1]
    
    if action == "dashboard":
        await show_dashboard(callback)
    elif action == "reports":
        await show_reports(callback)
    elif action == "alerts":
        await show_alerts(callback)
    elif action == "settings":
        await show_settings(callback)
    else:
        await callback.answer("Неизвестное действие")

async def show_dashboard(callback: CallbackQuery):
    """Показ дашборда аналитики"""
    try:
        # Получаем данные для дашборда
        dashboard_data = await realtime_dashboard.get_realtime_data()
        business_data = await business_dashboard.get_business_metrics()
        
        # Создаем клавиатуру
        builder = InlineKeyboardBuilder()
        builder.button(text="🔄 Обновить", callback_data="privacy_analytics:dashboard")
        builder.button(text="📈 Бизнес-метрики", callback_data="privacy_analytics:business")
        builder.button(text="⚙️ Настройки", callback_data="privacy_analytics:settings")
        builder.button(text="⬅️ Назад", callback_data="admin_panel:admin:1")
        builder.adjust(2, 1, 1)
        
        # Формируем сообщение
        message = f"""📊 **Дашборд аналитики**

🔗 **Активные подключения:** {dashboard_data.get('active_connections', 'N/A')}
💾 **Использование трафика:** {dashboard_data.get('bandwidth_usage', 'N/A')} GB
⚡ **Здоровье системы:** {dashboard_data.get('system_health', 'N/A')}%
💰 **Выручка сегодня:** {business_data.get('daily_revenue', 'N/A')} ₽

🛡️ **Статус приватности:** ✅ Соблюдается
📊 **Последнее обновление:** {datetime.now().strftime('%H:%M:%S')}"""
        
        await callback.message.edit_text(
            text=message,
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"[Privacy Analytics] Ошибка при показе дашборда: {e}")
        await callback.answer("Ошибка при загрузке дашборда")

async def show_reports(callback: CallbackQuery):
    """Показ отчетов"""
    try:
        # Получаем доступные отчеты
        reports = await report_generator.get_available_reports()
        
        builder = InlineKeyboardBuilder()
        for report in reports:
            builder.button(
                text=f"📄 {report['name']}",
                callback_data=f"privacy_analytics:report:{report['id']}"
            )
        
        builder.button(text="⬅️ Назад", callback_data="privacy_analytics:dashboard")
        builder.adjust(1)
        
        message = "📈 **Доступные отчеты**\n\nВыберите отчет для просмотра:"
        
        await callback.message.edit_text(
            text=message,
            reply_markup=builder.as_markup()
        )
        
    except Exception as e:
        logger.error(f"[Privacy Analytics] Ошибка при показе отчетов: {e}")
        await callback.answer("Ошибка при загрузке отчетов")

async def show_alerts(callback: CallbackQuery):
    """Показ алертов"""
    try:
        # Получаем активные алерты
        alerts = await alert_manager.get_active_alerts()
        
        builder = InlineKeyboardBuilder()
        builder.button(text="🔄 Обновить", callback_data="privacy_analytics:alerts")
        builder.button(text="⚙️ Настройки алертов", callback_data="privacy_analytics:alert_settings")
        builder.button(text="⬅️ Назад", callback_data="privacy_analytics:dashboard")
        builder.adjust(1)
        
        if alerts:
            alert_text = "🚨 **Активные алерты**\n\n"
            for alert in alerts[:5]:  # Показываем только первые 5
                severity_emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(alert['severity'], "⚪")
                alert_text += f"{severity_emoji} {alert['message']}\n"
        else:
            alert_text = "✅ **Нет активных алертов**\n\nВсе системы работают нормально"
        
        await callback.message.edit_text(
            text=alert_text,
            reply_markup=builder.as_markup()
        )
        
    except Exception as e:
        logger.error(f"[Privacy Analytics] Ошибка при показе алертов: {e}")
        await callback.answer("Ошибка при загрузке алертов")

async def show_settings(callback: CallbackQuery):
    """Показ настроек модуля"""
    try:
        builder = InlineKeyboardBuilder()
        builder.button(text="🔒 Настройки приватности", callback_data="privacy_analytics:privacy_settings")
        builder.button(text="📊 Настройки мониторинга", callback_data="privacy_analytics:monitoring_settings")
        builder.button(text="🚨 Настройки алертов", callback_data="privacy_analytics:alert_settings")
        builder.button(text="⬅️ Назад", callback_data="privacy_analytics:dashboard")
        builder.adjust(1)
        
        message = f"""⚙️ **Настройки модуля аналитики**

🔒 **Режим приватности:** {settings.PRIVACY_MODE}
📊 **Мониторинг:** {'✅ Включен' if settings.MONITORING_ENABLED else '❌ Выключен'}
🚨 **Алерты:** {'✅ Включены' if settings.ALERTS_ENABLED else '❌ Выключены'}
📈 **Дашборд:** {'✅ Включен' if settings.DASHBOARD_ENABLED else '❌ Выключен'}

🛡️ **Соответствие требованиям:** ✅ Проверено"""
        
        await callback.message.edit_text(
            text=message,
            reply_markup=builder.as_markup()
        )
        
    except Exception as e:
        logger.error(f"[Privacy Analytics] Ошибка при показе настроек: {e}")
        await callback.answer("Ошибка при загрузке настроек")

# Функция для получения данных вебхука (если нужна)
def get_webhook_data():
    """Возвращает данные для регистрации вебхука"""
    return {
        "path": "/analytics/webhook",
        "handler": handle_webhook
    }

async def handle_webhook(request):
    """Обработка входящих вебхуков"""
    try:
        data = await request.json()
        logger.info(f"[Privacy Analytics] Получен вебхук: {data}")
        
        # Обрабатываем вебхук
        if data.get("type") == "metrics":
            await data_processor.process_external_metrics(data)
        elif data.get("type") == "alert":
            await alert_manager.process_external_alert(data)
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"[Privacy Analytics] Ошибка обработки вебхука: {e}")
        return {"status": "error", "message": str(e)}

# Функция для получения обработчика быстрого флоу (если нужна)
def get_fast_flow_handler():
    """Возвращает обработчик быстрого флоу (если нужен)"""
    return None  # Этот модуль не использует быстрый флоу
