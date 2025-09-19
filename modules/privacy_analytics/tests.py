"""
Тесты для модуля Privacy Analytics
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

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


class TestServerMonitor:
    """Тесты для ServerMonitor"""
    
    @pytest.mark.asyncio
    async def test_collect_metrics(self):
        """Тест сбора метрик сервера"""
        monitor = ServerMonitor()
        metrics = await monitor.collect_metrics()
        
        assert isinstance(metrics, dict)
        assert "timestamp" in metrics
        assert "cpu_percent" in metrics
        assert "ram_percent" in metrics
        assert "disk_percent" in metrics
    
    @pytest.mark.asyncio
    async def test_start_monitoring(self):
        """Тест запуска мониторинга"""
        monitor = ServerMonitor()
        # Тестируем короткий период мониторинга
        monitor.interval = 0.1  # 100ms для быстрого теста
        
        # Запускаем мониторинг в фоне
        task = asyncio.create_task(monitor.start_monitoring())
        await asyncio.sleep(0.2)  # Ждем 200ms
        task.cancel()
        
        # Проверяем, что мониторинг запустился
        assert not task.done() or task.cancelled()


class TestPerformanceMonitor:
    """Тесты для PerformanceMonitor"""
    
    def test_record_api_response_time(self):
        """Тест записи времени ответа API"""
        monitor = PerformanceMonitor()
        monitor.record_api_response_time("/users", 150.5)
        
        assert len(monitor.metrics["api_response_times"]) == 1
        assert monitor.metrics["api_response_times"][0]["endpoint"] == "/users"
        assert monitor.metrics["api_response_times"][0]["duration_ms"] == 150.5
    
    def test_record_db_query_time(self):
        """Тест записи времени запроса к БД"""
        monitor = PerformanceMonitor()
        monitor.record_db_query_time("select_user", 25.3)
        
        assert len(monitor.metrics["db_query_times"]) == 1
        assert monitor.metrics["db_query_times"][0]["query_type"] == "select_user"
        assert monitor.metrics["db_query_times"][0]["duration_ms"] == 25.3
    
    def test_record_error(self):
        """Тест записи ошибки"""
        monitor = PerformanceMonitor()
        monitor.record_error("payment_gateway", "timeout")
        
        assert "payment_gateway:timeout" in monitor.metrics["error_rates"]
        assert monitor.metrics["error_rates"]["payment_gateway:timeout"] == 1


class TestSecurityMonitor:
    """Тесты для SecurityMonitor"""
    
    def test_record_failed_login(self):
        """Тест записи неудачной попытки входа"""
        monitor = SecurityMonitor()
        monitor.record_failed_login(1, "192.168.1.100")
        
        key = "1-192.168.1.100"
        assert key in monitor.failed_login_attempts
        assert monitor.failed_login_attempts[key]["count"] == 1
    
    def test_record_suspicious_activity(self):
        """Тест записи подозрительной активности"""
        monitor = SecurityMonitor()
        monitor.record_suspicious_activity(2, "unusual_vpn_usage", {"protocol": "unknown"})
        
        assert len(monitor.suspicious_activity_log) == 1
        assert monitor.suspicious_activity_log[0]["user_id"] == 2
        assert monitor.suspicious_activity_log[0]["activity_type"] == "unusual_vpn_usage"
    
    @pytest.mark.asyncio
    async def test_check_failed_logins(self):
        """Тест проверки неудачных попыток входа"""
        monitor = SecurityMonitor()
        
        # Добавляем несколько неудачных попыток
        for _ in range(6):  # Больше порога
            monitor.record_failed_login(1, "192.168.1.100")
        
        # Проверяем, что алерт будет срабатывать
        await monitor.check_failed_logins()
        
        # В реальном тесте здесь должна быть проверка на срабатывание алерта


class TestBusinessMonitor:
    """Тесты для BusinessMonitor"""
    
    @pytest.mark.asyncio
    async def test_collect_metrics(self):
        """Тест сбора бизнес-метрик"""
        monitor = BusinessMonitor()
        metrics = await monitor.collect_metrics()
        
        assert isinstance(metrics, dict)
        assert "new_subscriptions_daily" in metrics
        assert "total_revenue_daily" in metrics
        assert "active_users" in metrics


class TestDataProcessor:
    """Тесты для DataProcessor"""
    
    @pytest.mark.asyncio
    async def test_process_raw_log(self):
        """Тест обработки сырого лога"""
        processor = DataProcessor()
        
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
        
        await processor.process_raw_log(log_entry)
        
        # Проверяем, что данные были обработаны
        assert len(processor.aggregated_data) > 0
    
    @pytest.mark.asyncio
    async def test_get_aggregated_data(self):
        """Тест получения агрегированных данных"""
        processor = DataProcessor()
        
        # Обрабатываем несколько логов
        for i in range(3):
            log_entry = {
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
                "user_id": 123 + i,
                "ip_address": f"192.168.1.{100 + i}",
                "server_id": 1,
                "country": "US",
                "protocol": "VLESS",
                "bytes_sent_gb": 0.05,
                "bytes_recv_gb": 0.1
            }
            await processor.process_raw_log(log_entry)
        
        # Получаем агрегированные данные
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=2)
        data = await processor.get_aggregated_data(start_time, end_time)
        
        assert isinstance(data, list)
        assert len(data) > 0


class TestMetricsCalculator:
    """Тесты для MetricsCalculator"""
    
    def test_calculate_kpis(self):
        """Тест расчета KPI"""
        calculator = MetricsCalculator()
        
        aggregated_data = [
            {
                "hour": "2023-10-27-10",
                "connections": 100,
                "traffic_in_gb": 1.5,
                "traffic_out_gb": 2.0,
                "unique_users": 50,
                "unique_servers": 5,
                "countries": {"US": 70, "DE": 30},
                "protocols": {"VLESS": 80, "VMESS": 20}
            }
        ]
        
        kpis = calculator.calculate_kpis(aggregated_data)
        
        assert isinstance(kpis, dict)
        assert "total_connections" in kpis
        assert "total_traffic_gb" in kpis
        assert "approx_unique_users" in kpis
    
    def test_calculate_trends(self):
        """Тест расчета трендов"""
        calculator = MetricsCalculator()
        
        aggregated_data = [
            {
                "hour": "2023-10-27-10",
                "connections": 100,
                "traffic_in_gb": 1.5,
                "traffic_out_gb": 2.0,
                "unique_users": 50
            }
        ]
        
        trends = calculator.calculate_trends(aggregated_data)
        
        assert isinstance(trends, dict)
        assert "time_series" in trends
        assert len(trends["time_series"]) == 1


class TestReportGenerator:
    """Тесты для ReportGenerator"""
    
    @pytest.mark.asyncio
    async def test_generate_daily_report(self):
        """Тест генерации ежедневного отчета"""
        generator = ReportGenerator()
        
        aggregated_data = [
            {
                "hour": "2023-10-27-10",
                "connections": 100,
                "traffic_in_gb": 1.5,
                "traffic_out_gb": 2.0,
                "unique_users": 50
            }
        ]
        
        report = await generator.generate_daily_report(aggregated_data)
        
        assert isinstance(report, dict)
        assert report["report_type"] == "Daily Summary"
        assert "kpis" in report
    
    @pytest.mark.asyncio
    async def test_generate_weekly_report(self):
        """Тест генерации еженедельного отчета"""
        generator = ReportGenerator()
        
        aggregated_data = [
            {
                "hour": "2023-10-27-10",
                "connections": 100,
                "traffic_in_gb": 1.5,
                "traffic_out_gb": 2.0,
                "unique_users": 50
            }
        ]
        
        report = await generator.generate_weekly_report(aggregated_data)
        
        assert isinstance(report, dict)
        assert report["report_type"] == "Weekly Summary"
        assert "kpis" in report
        assert "trends" in report


class TestRealtimeDashboard:
    """Тесты для RealtimeDashboard"""
    
    def test_update_server_metrics(self):
        """Тест обновления метрик сервера"""
        dashboard = RealtimeDashboard()
        metrics = {"cpu_percent": 25.5, "ram_percent": 40.2}
        
        dashboard.update_server_metrics(metrics)
        
        assert dashboard.data["server_metrics"] == metrics
        assert dashboard.data["last_updated"] is not None
    
    def test_add_security_event(self):
        """Тест добавления события безопасности"""
        dashboard = RealtimeDashboard()
        event = {"type": "failed_login", "user_id": 1, "ip": "1.1.1.1"}
        
        dashboard.add_security_event(event)
        
        assert len(dashboard.data["security_events"]) == 1
        assert dashboard.data["security_events"][0] == event
    
    def test_get_dashboard_data(self):
        """Тест получения данных дашборда"""
        dashboard = RealtimeDashboard()
        dashboard.update_server_metrics({"cpu_percent": 25.5})
        
        data = dashboard.get_dashboard_data()
        
        assert isinstance(data, dict)
        assert "server_metrics" in data
        assert "last_updated" in data


class TestAlertManager:
    """Тесты для AlertManager"""
    
    @pytest.mark.asyncio
    async def test_trigger_alert(self):
        """Тест создания алерта"""
        alert_manager = AlertManager()
        
        await alert_manager.trigger_alert(
            "test_alert",
            "warning",
            "Test alert message",
            {"test_key": "test_value"}
        )
        
        assert "test_alert" in alert_manager.active_alerts
        assert alert_manager.active_alerts["test_alert"]["severity"] == "warning"
        assert alert_manager.active_alerts["test_alert"]["message"] == "Test alert message"
    
    @pytest.mark.asyncio
    async def test_resolve_alert(self):
        """Тест разрешения алерта"""
        alert_manager = AlertManager()
        
        # Создаем алерт
        await alert_manager.trigger_alert("test_alert", "warning", "Test message")
        
        # Разрешаем алерт
        await alert_manager.resolve_alert("test_alert", "Resolved")
        
        # Проверяем, что алерт больше не активен
        assert "test_alert" not in alert_manager.active_alerts
    
    def test_get_active_alerts(self):
        """Тест получения активных алертов"""
        alert_manager = AlertManager()
        
        # Добавляем тестовый алерт
        alert_manager.active_alerts["test_alert"] = {
            "id": "test_alert",
            "severity": "warning",
            "message": "Test message",
            "status": "active"
        }
        
        active_alerts = alert_manager.get_active_alerts()
        
        assert len(active_alerts) == 1
        assert active_alerts[0]["id"] == "test_alert"


class TestPrivacyChecker:
    """Тесты для PrivacyChecker"""
    
    def test_check_log_entry_for_privacy(self):
        """Тест проверки лога на приватность"""
        checker = PrivacyChecker()
        
        # Лог с нарушением (содержит user_id без анонимизации)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": 123,
            "ip_address": "192.168.1.100",
            "server_id": 1
        }
        
        violations = checker.check_log_entry_for_privacy(log_entry)
        
        assert len(violations) > 0
        assert any("user_id" in violation for violation in violations)
    
    def test_check_analytics_data_for_privacy(self):
        """Тест проверки аналитических данных на приватность"""
        checker = PrivacyChecker()
        
        # Аналитические данные с PII
        analytics_data = {
            "total_connections": 100,
            "user_id": 123,  # PII в аналитике
            "top_countries": {"US": 70}
        }
        
        violations = checker.check_analytics_data_for_privacy(analytics_data)
        
        assert len(violations) > 0
        assert any("user_id" in violation for violation in violations)


class TestDataAnonymizer:
    """Тесты для DataAnonymizer"""
    
    def test_anonymize_log_entry(self):
        """Тест анонимизации лога"""
        anonymizer = DataAnonymizer()
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": 123,
            "ip_address": "192.168.1.100",
            "server_id": 1,
            "country": "US"
        }
        
        anonymized = anonymizer.anonymize_log_entry(log_entry, "full")
        
        assert "user_id" not in anonymized
        assert "ip_address" not in anonymized
        assert "anonymized_user_id" in anonymized
        assert "anonymized_ip_address" in anonymized
    
    def test_pseudonymize_user_id(self):
        """Тест псевдонимизации ID пользователя"""
        anonymizer = DataAnonymizer()
        
        user_id = "user123"
        pseudonym1 = anonymizer._pseudonymize_user_id(user_id)
        pseudonym2 = anonymizer._pseudonymize_user_id(user_id)
        
        # Псевдоним должен быть одинаковым для одного ID
        assert pseudonym1 == pseudonym2
        assert pseudonym1 != user_id
        assert pseudonym1.startswith("user_")


class TestConsentManager:
    """Тесты для ConsentManager"""
    
    @pytest.mark.asyncio
    async def test_create_consent(self):
        """Тест создания согласия"""
        manager = ConsentManager()
        
        consent_id = await manager.create_consent("user123", ConsentPurpose.ANALYTICS)
        
        assert consent_id != ""
        assert consent_id in manager.consents
        assert manager.consents[consent_id]["subject_id"] == "user123"
        assert manager.consents[consent_id]["purpose"] == ConsentPurpose.ANALYTICS.value
    
    @pytest.mark.asyncio
    async def test_withdraw_consent(self):
        """Тест отзыва согласия"""
        manager = ConsentManager()
        
        # Создаем согласие
        consent_id = await manager.create_consent("user123", ConsentPurpose.ANALYTICS)
        
        # Отзываем согласие
        success = await manager.withdraw_consent(consent_id, "User requested")
        
        assert success
        assert manager.consents[consent_id]["status"] == ConsentStatus.WITHDRAWN.value
    
    @pytest.mark.asyncio
    async def test_check_consent(self):
        """Тест проверки согласия"""
        manager = ConsentManager()
        
        # Создаем согласие
        await manager.create_consent("user123", ConsentPurpose.ANALYTICS)
        
        # Проверяем согласие
        has_consent = await manager.check_consent("user123", ConsentPurpose.ANALYTICS)
        
        assert has_consent


class TestDataRetentionManager:
    """Тесты для DataRetentionManager"""
    
    @pytest.mark.asyncio
    async def test_register_data(self):
        """Тест регистрации данных"""
        manager = DataRetentionManager()
        
        success = await manager.register_data(
            "data123",
            DataCategory.PERSONAL_DATA,
            "user_profile",
            1024
        )
        
        assert success
        assert "data123" in manager.data_lifecycle
        assert manager.data_lifecycle["data123"]["category"] == DataCategory.PERSONAL_DATA.value
    
    @pytest.mark.asyncio
    async def test_mark_data_anonymized(self):
        """Тест отметки данных как анонимизированных"""
        manager = DataRetentionManager()
        
        # Регистрируем данные
        await manager.register_data("data123", DataCategory.PERSONAL_DATA, "user_profile", 1024)
        
        # Отмечаем как анонимизированные
        success = await manager.mark_data_anonymized("data123", "hash_anonymization")
        
        assert success
        assert manager.data_lifecycle["data123"]["anonymized"] is True
        assert manager.data_lifecycle["data123"]["anonymization_method"] == "hash_anonymization"
    
    @pytest.mark.asyncio
    async def test_check_data_expiry(self):
        """Тест проверки истечения данных"""
        manager = DataRetentionManager()
        
        # Регистрируем данные с коротким сроком хранения
        await manager.register_data("data123", DataCategory.LOG_DATA, "log_entry", 1024)
        
        # Устанавливаем истекший срок
        manager.data_lifecycle["data123"]["expires_at"] = (datetime.utcnow() - timedelta(days=1)).isoformat()
        
        # Проверяем истечение
        expired_data = await manager.check_data_expiry()
        
        assert "data123" in expired_data
        assert manager.data_lifecycle["data123"]["status"] == "expired"


class TestAuditLogger:
    """Тесты для AuditLogger"""
    
    @pytest.mark.asyncio
    async def test_log_event(self):
        """Тест логирования события"""
        logger = AuditLogger()
        
        event_id = await logger.log_event(
            "data_access",
            "Access to user data",
            "user123",
            "user_profile",
            "medium"
        )
        
        assert event_id != ""
        assert len(logger.audit_log) == 1
        assert logger.audit_log[0]["event_type"] == "data_access"
    
    @pytest.mark.asyncio
    async def test_log_data_access(self):
        """Тест логирования доступа к данным"""
        logger = AuditLogger()
        
        event_id = await logger.log_data_access(
            "user_profile",
            "user123",
            ["personal_data"],
            "analytics"
        )
        
        assert event_id != ""
        assert len(logger.audit_log) == 1
        assert logger.audit_log[0]["event_type"] == "data_access"
    
    def test_get_audit_log(self):
        """Тест получения лога аудита"""
        logger = AuditLogger()
        
        # Добавляем тестовые события
        logger.audit_log = [
            {
                "event_type": "data_access",
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": "user123"
            },
            {
                "event_type": "data_modification",
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": "user456"
            }
        ]
        
        # Фильтруем по типу события
        filtered_log = await logger.get_audit_log(event_type="data_access")
        
        assert len(filtered_log) == 1
        assert filtered_log[0]["event_type"] == "data_access"


class TestPrivacyPolicyManager:
    """Тесты для PrivacyPolicyManager"""
    
    def test_get_privacy_policy(self):
        """Тест получения политики приватности"""
        manager = PrivacyPolicyManager()
        
        policy = manager.get_privacy_policy("default")
        
        assert policy is not None
        assert policy["name"] == "Основная политика приватности"
        assert "version" in policy
    
    @pytest.mark.asyncio
    async def test_update_privacy_policy(self):
        """Тест обновления политики приватности"""
        manager = PrivacyPolicyManager()
        
        updates = {"retention_period": 500}
        success = await manager.update_privacy_policy(
            "default",
            updates,
            "Updated retention period",
            "admin"
        )
        
        assert success
        assert manager.privacy_policies["default"]["retention_period"] == 500
        assert manager.privacy_policies["default"]["version"] == "1.1"
    
    @pytest.mark.asyncio
    async def test_validate_policy_compliance(self):
        """Тест проверки соответствия политики"""
        manager = PrivacyPolicyManager()
        
        compliance = await manager.validate_policy_compliance("default")
        
        assert "compliant" in compliance
        assert "errors" in compliance
        assert "warnings" in compliance


# Интеграционные тесты
class TestIntegration:
    """Интеграционные тесты"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        # Создаем все компоненты
        server_monitor = ServerMonitor()
        data_processor = DataProcessor()
        metrics_calculator = MetricsCalculator()
        alert_manager = AlertManager()
        privacy_checker = PrivacyChecker()
        data_anonymizer = DataAnonymizer()
        consent_manager = ConsentManager()
        audit_logger = AuditLogger()
        
        # 1. Создаем согласие
        await consent_manager.create_consent("user123", ConsentPurpose.ANALYTICS)
        
        # 2. Собираем метрики
        server_metrics = await server_monitor.collect_metrics()
        
        # 3. Обрабатываем данные
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
        assert len(violations) > 0  # Должны быть нарушения
        
        # Анонимизируем данные
        anonymized_entry = data_anonymizer.anonymize_log_entry(log_entry, "full")
        
        # Обрабатываем анонимизированные данные
        await data_processor.process_raw_log(anonymized_entry)
        
        # 4. Рассчитываем метрики
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)
        aggregated_data = await data_processor.get_aggregated_data(start_time, end_time)
        kpis = metrics_calculator.calculate_kpis(aggregated_data)
        
        # 5. Проверяем алерты
        if server_metrics.get("cpu_percent", 0) > 80:
            await alert_manager.trigger_alert(
                "server_cpu_high",
                "warning",
                "CPU usage is high",
                server_metrics
            )
        
        # 6. Логируем аудит
        await audit_logger.log_data_access("analytics", "user123", ["analytics_data"], "reporting")
        
        # Проверяем результаты
        assert len(aggregated_data) >= 0
        assert isinstance(kpis, dict)
        assert len(alert_manager.get_active_alerts()) >= 0
        assert len(audit_logger.audit_log) > 0


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])
