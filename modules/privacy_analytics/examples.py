"""
Примеры использования модуля Privacy Analytics
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

# Импорты компонентов модуля
from .monitoring import ServerMonitor, PerformanceMonitor, SecurityMonitor, BusinessMonitor
from .analytics import DataProcessor, MetricsCalculator, ReportGenerator
from .dashboards import RealtimeDashboard, BusinessDashboard, AdminDashboard
from .alerts import AlertManager, TelegramChannel, EmailChannel
from .privacy import (
    PrivacyChecker, DataAnonymizer, GDPRCompliance,
    AuditLogger, ConsentManager, DataRetentionManager, PrivacyPolicyManager,
    ConsentPurpose, ConsentMethod, DataCategory, RetentionPolicy
)


async def example_monitoring():
    """Пример использования системы мониторинга"""
    print("=== Пример системы мониторинга ===")
    
    # Мониторинг сервера
    server_monitor = ServerMonitor()
    server_metrics = await server_monitor.collect_metrics()
    print(f"Метрики сервера: {server_metrics}")
    
    # Мониторинг производительности
    performance_monitor = PerformanceMonitor()
    performance_monitor.record_api_response_time("/users", 150.5)
    performance_monitor.record_db_query_time("select_user", 25.3)
    performance_monitor.record_error("payment_gateway", "timeout")
    print(f"Метрики производительности: {performance_monitor.metrics}")
    
    # Мониторинг безопасности
    security_monitor = SecurityMonitor()
    security_monitor.record_failed_login(1, "192.168.1.100")
    security_monitor.record_suspicious_activity(2, "unusual_vpn_usage", {"protocol": "unknown"})
    print("События безопасности зарегистрированы")
    
    # Мониторинг бизнеса
    business_monitor = BusinessMonitor()
    business_metrics = await business_monitor.collect_metrics()
    print(f"Бизнес-метрики: {business_metrics}")


async def example_analytics():
    """Пример использования системы аналитики"""
    print("\n=== Пример системы аналитики ===")
    
    # Обработка данных
    data_processor = DataProcessor()
    
    # Обрабатываем несколько логов
    log_entries = [
        {
            "timestamp": datetime.now().isoformat(),
            "user_id": 123,
            "ip_address": "192.168.1.100",
            "server_id": 1,
            "country": "US",
            "protocol": "VLESS",
            "bytes_sent_gb": 0.05,
            "bytes_recv_gb": 0.1
        },
        {
            "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "user_id": 124,
            "ip_address": "192.168.1.101",
            "server_id": 2,
            "country": "DE",
            "protocol": "VLESS",
            "bytes_sent_gb": 0.02,
            "bytes_recv_gb": 0.03
        }
    ]
    
    for log_entry in log_entries:
        await data_processor.process_raw_log(log_entry)
    
    # Получаем агрегированные данные
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=2)
    aggregated_data = await data_processor.get_aggregated_data(start_time, end_time)
    print(f"Агрегированные данные: {aggregated_data}")
    
    # Расчет метрик
    metrics_calculator = MetricsCalculator()
    kpis = metrics_calculator.calculate_kpis(aggregated_data)
    trends = metrics_calculator.calculate_trends(aggregated_data)
    print(f"KPI: {kpis}")
    print(f"Тренды: {trends}")
    
    # Генерация отчетов
    report_generator = ReportGenerator()
    daily_report = await report_generator.generate_daily_report(aggregated_data)
    print(f"Ежедневный отчет: {daily_report}")


async def example_dashboards():
    """Пример использования дашбордов"""
    print("\n=== Пример дашбордов ===")
    
    # Дашборд реального времени
    realtime_dashboard = RealtimeDashboard()
    realtime_dashboard.update_server_metrics({"cpu_percent": 25.5, "ram_percent": 40.2})
    realtime_dashboard.update_performance_metrics({"api_avg_response_ms": 120.5, "error_rate": 0.01})
    realtime_dashboard.add_security_event({"type": "failed_login", "user_id": 1, "ip": "1.1.1.1"})
    realtime_dashboard.update_business_kpis({"active_users": 150, "new_subs_today": 5})
    
    dashboard_data = realtime_dashboard.get_dashboard_data()
    print(f"Данные дашборда реального времени: {dashboard_data}")


async def example_alerts():
    """Пример использования системы алертов"""
    print("\n=== Пример системы алертов ===")
    
    # Создаем менеджер алертов
    alert_manager = AlertManager()
    
    # Регистрируем каналы уведомлений
    telegram_channel = TelegramChannel("YOUR_BOT_TOKEN", "YOUR_CHAT_ID")
    email_channel = EmailChannel(
        "smtp.example.com", 587, "user@example.com", "password",
        "sender@example.com", ["recipient@example.com"]
    )
    
    # Добавляем каналы в менеджер
    alert_manager.notification_channels["telegram"] = telegram_channel
    alert_manager.notification_channels["email"] = email_channel
    
    # Создаем алерт
    await alert_manager.trigger_alert(
        "server_cpu_high",
        "warning",
        "CPU usage is high",
        {"server_id": 1, "cpu_percent": 85.2}
    )
    
    # Создаем критический алерт
    await alert_manager.trigger_alert(
        "server_cpu_critical",
        "critical",
        "CPU usage is CRITICAL",
        {"server_id": 1, "cpu_percent": 95.1}
    )
    
    # Получаем активные алерты
    active_alerts = alert_manager.get_active_alerts()
    print(f"Активные алерты: {active_alerts}")
    
    # Разрешаем алерт
    await alert_manager.resolve_alert("server_cpu_high", "CPU usage returned to normal")
    print("Алерт разрешен")


async def example_privacy():
    """Пример использования системы приватности"""
    print("\n=== Пример системы приватности ===")
    
    # Проверка приватности
    privacy_checker = PrivacyChecker()
    
    # Проверяем лог на соответствие политикам
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": 123,
        "ip_address": "192.168.1.100",
        "server_id": 1
    }
    
    violations = privacy_checker.check_log_entry_for_privacy(log_entry)
    print(f"Нарушения приватности: {violations}")
    
    # Анонимизация данных
    data_anonymizer = DataAnonymizer()
    anonymized_entry = data_anonymizer.anonymize_log_entry(log_entry, "full")
    print(f"Анонимизированная запись: {anonymized_entry}")
    
    # Управление согласиями
    consent_manager = ConsentManager()
    consent_id = await consent_manager.create_consent("user123", ConsentPurpose.ANALYTICS)
    print(f"Создано согласие: {consent_id}")
    
    # Проверяем согласие
    has_consent = await consent_manager.check_consent("user123", ConsentPurpose.ANALYTICS)
    print(f"Есть согласие: {has_consent}")
    
    # Управление хранением данных
    retention_manager = DataRetentionManager()
    await retention_manager.register_data(
        "data_123",
        DataCategory.PERSONAL_DATA,
        "user_profile",
        1024
    )
    print("Данные зарегистрированы для отслеживания хранения")
    
    # Аудит
    audit_logger = AuditLogger()
    await audit_logger.log_data_access("user_profile", "user123", ["personal_data"], "analytics")
    print("Событие аудита зарегистрировано")


async def example_api_usage():
    """Пример использования API"""
    print("\n=== Пример использования API ===")
    
    # В реальном приложении эти запросы будут выполняться через HTTP
    # Здесь мы показываем, как использовать компоненты напрямую
    
    # Получение метрик сервера
    server_monitor = ServerMonitor()
    server_metrics = await server_monitor.collect_metrics()
    print(f"API: Метрики сервера: {server_metrics}")
    
    # Получение KPI
    data_processor = DataProcessor()
    metrics_calculator = MetricsCalculator()
    
    # Обрабатываем данные
    await data_processor.process_raw_log({
        "timestamp": datetime.now().isoformat(),
        "user_id": 123,
        "ip_address": "192.168.1.100",
        "server_id": 1,
        "country": "US",
        "protocol": "VLESS",
        "bytes_sent_gb": 0.05,
        "bytes_recv_gb": 0.1
    })
    
    # Получаем агрегированные данные
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    aggregated_data = await data_processor.get_aggregated_data(start_time, end_time)
    
    # Рассчитываем KPI
    kpis = metrics_calculator.calculate_kpis(aggregated_data)
    print(f"API: KPI: {kpis}")


async def example_integration():
    """Пример интеграции всех компонентов"""
    print("\n=== Пример интеграции всех компонентов ===")
    
    # Создаем все компоненты
    server_monitor = ServerMonitor()
    performance_monitor = PerformanceMonitor()
    security_monitor = SecurityMonitor()
    business_monitor = BusinessMonitor()
    data_processor = DataProcessor()
    metrics_calculator = MetricsCalculator()
    report_generator = ReportGenerator()
    alert_manager = AlertManager()
    privacy_checker = PrivacyChecker()
    data_anonymizer = DataAnonymizer()
    consent_manager = ConsentManager()
    retention_manager = DataRetentionManager()
    audit_logger = AuditLogger()
    
    # Создаем дашборды
    realtime_dashboard = RealtimeDashboard()
    business_dashboard = BusinessDashboard(data_processor, metrics_calculator)
    admin_dashboard = AdminDashboard(data_processor, metrics_calculator)
    
    print("Все компоненты инициализированы")
    
    # Симулируем работу системы
    print("Симуляция работы системы...")
    
    # 1. Собираем метрики
    server_metrics = await server_monitor.collect_metrics()
    business_metrics = await business_monitor.collect_metrics()
    
    # 2. Обрабатываем данные
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": 123,
        "ip_address": "192.168.1.100",
        "server_id": 1,
        "country": "US",
        "protocol": "VLESS",
        "bytes_sent_gb": 0.05,
        "bytes_recv_gb": 0.1
    }
    
    # Проверяем приватность
    violations = privacy_checker.check_log_entry_for_privacy(log_entry)
    if violations:
        print(f"Нарушения приватности: {violations}")
        return
    
    # Анонимизируем данные
    anonymized_entry = data_anonymizer.anonymize_log_entry(log_entry, "full")
    
    # Обрабатываем анонимизированные данные
    await data_processor.process_raw_log(anonymized_entry)
    
    # 3. Обновляем дашборды
    realtime_dashboard.update_server_metrics(server_metrics)
    realtime_dashboard.update_business_kpis(business_metrics)
    
    # 4. Проверяем алерты
    if server_metrics.get("cpu_percent", 0) > 80:
        await alert_manager.trigger_alert(
            "server_cpu_high",
            "warning",
            "CPU usage is high",
            server_metrics
        )
    
    # 5. Генерируем отчеты
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    aggregated_data = await data_processor.get_aggregated_data(start_time, end_time)
    kpis = metrics_calculator.calculate_kpis(aggregated_data)
    daily_report = await report_generator.generate_daily_report(aggregated_data)
    
    # 6. Логируем аудит
    await audit_logger.log_data_access("analytics", "user123", ["analytics_data"], "reporting")
    
    print("Интеграция завершена успешно")
    print(f"KPI: {kpis}")
    print(f"Активные алерты: {len(alert_manager.get_active_alerts())}")


async def main():
    """Главная функция с примерами"""
    print("Privacy Analytics Module - Примеры использования")
    print("=" * 50)
    
    try:
        await example_monitoring()
        await example_analytics()
        await example_dashboards()
        await example_alerts()
        await example_privacy()
        await example_api_usage()
        await example_integration()
        
        print("\n" + "=" * 50)
        print("Все примеры выполнены успешно!")
        
    except Exception as e:
        print(f"Ошибка при выполнении примеров: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
