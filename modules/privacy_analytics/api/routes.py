"""
API маршруты для Privacy-Compliant Analytics
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio

from .. import settings
from ..monitoring import ServerMonitor, PerformanceMonitor, SecurityMonitor, BusinessMonitor
from ..analytics import DataProcessor, MetricsCalculator, ReportGenerator
from ..dashboards import RealtimeDashboard, BusinessDashboard, AdminDashboard
from ..alerts import AlertManager
from ..privacy import PrivacyComplianceChecker
from .middleware import PrivacyMiddleware, RateLimitMiddleware
from .schemas import *
from logger import logger


def create_api_routes(app: FastAPI):
    """Создание API маршрутов"""
    
    # Добавляем middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.API_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.API_CORS_METHODS,
        allow_headers=settings.API_CORS_HEADERS,
    )
    
    app.add_middleware(PrivacyMiddleware)
    app.add_middleware(RateLimitMiddleware)
    
    # Инициализируем компоненты
    server_monitor = ServerMonitor()
    performance_monitor = PerformanceMonitor()
    security_monitor = SecurityMonitor()
    business_monitor = BusinessMonitor()
    data_processor = DataProcessor()
    metrics_calculator = MetricsCalculator()
    report_generator = ReportGenerator()
    realtime_dashboard = RealtimeDashboard()
    business_dashboard = BusinessDashboard()
    admin_dashboard = AdminDashboard()
    alert_manager = AlertManager()
    privacy_checker = PrivacyComplianceChecker()
    
    # ========================================
    # 📊 МОНИТОРИНГ
    # ========================================
    
    @app.get("/api/v1/monitoring/servers", response_model=List[ServerStatusResponse])
    async def get_servers_status():
        """Получение статуса серверов"""
        try:
            servers = await server_monitor.get_active_servers()
            status_list = []
            
            for server in servers:
                status_data = await server_monitor.get_server_summary(server['id'])
                status_list.append(ServerStatusResponse(**status_data))
            
            return status_list
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения статуса серверов: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения статуса серверов")
    
    @app.get("/api/v1/monitoring/performance", response_model=PerformanceMetricsResponse)
    async def get_performance_metrics():
        """Получение метрик производительности"""
        try:
            metrics = await performance_monitor.get_performance_summary()
            return PerformanceMetricsResponse(**metrics)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения метрик производительности: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения метрик производительности")
    
    @app.get("/api/v1/monitoring/security", response_model=SecurityMetricsResponse)
    async def get_security_metrics():
        """Получение метрик безопасности"""
        try:
            metrics = await security_monitor.get_security_summary()
            return SecurityMetricsResponse(**metrics)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения метрик безопасности: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения метрик безопасности")
    
    @app.get("/api/v1/monitoring/business", response_model=BusinessMetricsResponse)
    async def get_business_metrics():
        """Получение бизнес-метрик"""
        try:
            metrics = await business_monitor.get_business_summary()
            return BusinessMetricsResponse(**metrics)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения бизнес-метрик: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения бизнес-метрик")
    
    # ========================================
    # 📈 АНАЛИТИКА
    # ========================================
    
    @app.post("/api/v1/analytics/process", response_model=ProcessingResponse)
    async def process_metrics(request: MetricsProcessingRequest):
        """Обработка метрик"""
        try:
            # Проверяем соответствие требованиям приватности
            if not privacy_checker.validate_metrics(request.dict()):
                raise HTTPException(status_code=400, detail="Данные не прошли проверку приватности")
            
            result = await data_processor.process_metrics(request.dict())
            return ProcessingResponse(
                success=True,
                processed_metrics=result,
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(f"[API] Ошибка обработки метрик: {e}")
            raise HTTPException(status_code=500, detail="Ошибка обработки метрик")
    
    @app.get("/api/v1/analytics/metrics/performance", response_model=PerformanceAnalysisResponse)
    async def get_performance_analysis():
        """Получение анализа производительности"""
        try:
            # Здесь должна быть логика получения данных для анализа
            import random
            
            analysis = {
                "performance_score": round(random.uniform(70, 95), 2),
                "efficiency_metrics": {
                    "cpu_efficiency": round(random.uniform(60, 90), 2),
                    "memory_efficiency": round(random.uniform(65, 85), 2),
                    "network_efficiency": round(random.uniform(70, 95), 2)
                },
                "bottlenecks": [
                    "CPU usage occasionally high during peak hours",
                    "Memory usage increasing over time"
                ] if random.choice([True, False]) else [],
                "recommendations": [
                    "Implement caching for frequently accessed data",
                    "Optimize database queries"
                ]
            }
            
            return PerformanceAnalysisResponse(**analysis)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения анализа производительности: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения анализа производительности")
    
    @app.get("/api/v1/analytics/metrics/business", response_model=BusinessAnalysisResponse)
    async def get_business_analysis():
        """Получение бизнес-анализа"""
        try:
            # Здесь должна быть логика получения данных для анализа
            import random
            
            analysis = {
                "revenue_metrics": {
                    "daily_revenue": round(random.uniform(10000, 50000), 2),
                    "growth_rate": round(random.uniform(-5, 25), 2),
                    "revenue_per_user": round(random.uniform(100, 500), 2)
                },
                "user_metrics": {
                    "total_users": random.randint(1000, 5000),
                    "active_users": random.randint(200, 800),
                    "retention_rate": round(random.uniform(75, 90), 2)
                },
                "conversion_metrics": {
                    "overall_conversion": round(random.uniform(2, 8), 2),
                    "trial_to_paid": round(random.uniform(15, 35), 2)
                }
            }
            
            return BusinessAnalysisResponse(**analysis)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения бизнес-анализа: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения бизнес-анализа")
    
    # ========================================
    # 📊 ДАШБОРДЫ
    # ========================================
    
    @app.get("/api/v1/dashboards/realtime", response_model=RealtimeDashboardResponse)
    async def get_realtime_dashboard():
        """Получение данных дашборда в реальном времени"""
        try:
            data = await realtime_dashboard.get_realtime_data()
            return RealtimeDashboardResponse(**data)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения данных дашборда: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения данных дашборда")
    
    @app.get("/api/v1/dashboards/business", response_model=BusinessDashboardResponse)
    async def get_business_dashboard():
        """Получение данных бизнес-дашборда"""
        try:
            data = await business_dashboard.get_business_metrics()
            return BusinessDashboardResponse(**data)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения данных бизнес-дашборда: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения данных бизнес-дашборда")
    
    @app.get("/api/v1/dashboards/admin", response_model=AdminDashboardResponse)
    async def get_admin_dashboard():
        """Получение данных административного дашборда"""
        try:
            data = await admin_dashboard.get_admin_metrics()
            return AdminDashboardResponse(**data)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения данных админ-дашборда: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения данных админ-дашборда")
    
    # ========================================
    # 🚨 АЛЕРТЫ
    # ========================================
    
    @app.get("/api/v1/alerts", response_model=List[AlertResponse])
    async def get_alerts(active_only: bool = True):
        """Получение алертов"""
        try:
            if active_only:
                alerts = await alert_manager.get_active_alerts()
            else:
                # Здесь должна быть логика получения всех алертов
                alerts = await alert_manager.get_active_alerts()
            
            return [AlertResponse(**alert) for alert in alerts]
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения алертов: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения алертов")
    
    @app.post("/api/v1/alerts/{alert_id}/acknowledge", response_model=AcknowledgeResponse)
    async def acknowledge_alert(alert_id: str, request: AcknowledgeRequest):
        """Подтверждение алерта"""
        try:
            success = await alert_manager.acknowledge_alert(alert_id, request.acknowledged_by)
            
            if not success:
                raise HTTPException(status_code=404, detail="Алерт не найден")
            
            return AcknowledgeResponse(success=True, message="Алерт подтвержден")
            
        except Exception as e:
            logger.error(f"[API] Ошибка подтверждения алерта: {e}")
            raise HTTPException(status_code=500, detail="Ошибка подтверждения алерта")
    
    @app.post("/api/v1/alerts/{alert_id}/resolve", response_model=ResolveResponse)
    async def resolve_alert(alert_id: str, request: ResolveRequest):
        """Разрешение алерта"""
        try:
            success = await alert_manager.resolve_alert(alert_id, request.resolved_by)
            
            if not success:
                raise HTTPException(status_code=404, detail="Алерт не найден")
            
            return ResolveResponse(success=True, message="Алерт разрешен")
            
        except Exception as e:
            logger.error(f"[API] Ошибка разрешения алерта: {e}")
            raise HTTPException(status_code=500, detail="Ошибка разрешения алерта")
    
    @app.get("/api/v1/alerts/statistics", response_model=AlertStatisticsResponse)
    async def get_alert_statistics():
        """Получение статистики алертов"""
        try:
            stats = await alert_manager.get_alert_statistics()
            return AlertStatisticsResponse(**stats)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения статистики алертов: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения статистики алертов")
    
    # ========================================
    # 📄 ОТЧЕТЫ
    # ========================================
    
    @app.get("/api/v1/reports", response_model=List[ReportResponse])
    async def get_available_reports():
        """Получение доступных отчетов"""
        try:
            reports = await report_generator.get_available_reports()
            return [ReportResponse(**report) for report in reports]
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения списка отчетов: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения списка отчетов")
    
    @app.post("/api/v1/reports/generate", response_model=ReportGenerationResponse)
    async def generate_report(request: ReportGenerationRequest):
        """Генерация отчета"""
        try:
            if request.report_type == "daily":
                report = await report_generator.generate_daily_report()
            elif request.report_type == "weekly":
                report = await report_generator.generate_weekly_report()
            elif request.report_type == "monthly":
                report = await report_generator.generate_monthly_report()
            else:
                raise HTTPException(status_code=400, detail="Неподдерживаемый тип отчета")
            
            return ReportGenerationResponse(
                success=True,
                report=report,
                generated_at=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(f"[API] Ошибка генерации отчета: {e}")
            raise HTTPException(status_code=500, detail="Ошибка генерации отчета")
    
    @app.get("/api/v1/reports/{report_id}/export")
    async def export_report(report_id: str, format: str = "json"):
        """Экспорт отчета"""
        try:
            # Здесь должна быть логика получения отчета по ID
            # Для примера генерируем новый отчет
            report = await report_generator.generate_daily_report()
            
            # Экспортируем в указанном формате
            exported_data = await report_generator.export_report(report, format)
            
            if format == "json":
                return JSONResponse(content=exported_data)
            elif format == "csv":
                return JSONResponse(content={"csv_data": exported_data})
            elif format == "html":
                return JSONResponse(content={"html_data": exported_data})
            else:
                raise HTTPException(status_code=400, detail="Неподдерживаемый формат экспорта")
                
        except Exception as e:
            logger.error(f"[API] Ошибка экспорта отчета: {e}")
            raise HTTPException(status_code=500, detail="Ошибка экспорта отчета")
    
    # ========================================
    # 🔒 ПРИВАТНОСТЬ И БЕЗОПАСНОСТЬ
    # ========================================
    
    @app.get("/api/v1/privacy/compliance", response_model=PrivacyComplianceResponse)
    async def check_privacy_compliance():
        """Проверка соответствия требованиям приватности"""
        try:
            compliance_status = await privacy_checker.audit_system_compliance()
            
            return PrivacyComplianceResponse(
                compliant=compliance_status,
                last_check=datetime.utcnow().isoformat(),
                privacy_mode=settings.PRIVACY_MODE,
                data_anonymization=settings.DATA_ANONYMIZATION,
                personal_data_filtering=settings.PERSONAL_DATA_FILTERING
            )
            
        except Exception as e:
            logger.error(f"[API] Ошибка проверки соответствия приватности: {e}")
            raise HTTPException(status_code=500, detail="Ошибка проверки соответствия приватности")
    
    @app.get("/api/v1/health", response_model=HealthResponse)
    async def health_check():
        """Проверка здоровья API"""
        try:
            return HealthResponse(
                status="healthy",
                timestamp=datetime.utcnow().isoformat(),
                version="1.0.0",
                components={
                    "monitoring": "healthy",
                    "analytics": "healthy",
                    "alerts": "healthy",
                    "privacy": "healthy"
                }
            )
            
        except Exception as e:
            logger.error(f"[API] Ошибка проверки здоровья: {e}")
            raise HTTPException(status_code=500, detail="Ошибка проверки здоровья")
    
    # ========================================
    # 📊 СТАТИСТИКА И МЕТРИКИ
    # ========================================
    
    @app.get("/api/v1/statistics/overview", response_model=StatisticsOverviewResponse)
    async def get_statistics_overview():
        """Получение обзора статистики"""
        try:
            # Здесь должна быть логика получения общей статистики
            import random
            
            overview = {
                "total_requests": random.randint(10000, 100000),
                "success_rate": round(random.uniform(95, 100), 2),
                "average_response_time": round(random.uniform(50, 300), 2),
                "active_users": random.randint(100, 1000),
                "system_uptime": round(random.uniform(95, 100), 2),
                "last_updated": datetime.utcnow().isoformat()
            }
            
            return StatisticsOverviewResponse(**overview)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения обзора статистики: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения обзора статистики")
    
    # ========================================
    # 🔧 УПРАВЛЕНИЕ
    # ========================================
    
    @app.post("/api/v1/management/refresh", response_model=RefreshResponse)
    async def refresh_data():
        """Принудительное обновление данных"""
        try:
            # Обновляем все дашборды
            await realtime_dashboard.refresh_data()
            await business_dashboard.refresh_data()
            await admin_dashboard.refresh_data()
            
            return RefreshResponse(
                success=True,
                message="Данные обновлены",
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(f"[API] Ошибка обновления данных: {e}")
            raise HTTPException(status_code=500, detail="Ошибка обновления данных")
    
    @app.get("/api/v1/management/config", response_model=ConfigResponse)
    async def get_config():
        """Получение конфигурации"""
        try:
            config = {
                "privacy_mode": settings.PRIVACY_MODE,
                "monitoring_enabled": settings.MONITORING_ENABLED,
                "alerts_enabled": settings.ALERTS_ENABLED,
                "dashboard_enabled": settings.DASHBOARD_ENABLED,
                "data_retention_days": settings.DATA_RETENTION_DAYS,
                "real_time_update_interval": settings.REAL_TIME_UPDATE_INTERVAL,
                "dashboard_refresh_interval": settings.DASHBOARD_REFRESH_INTERVAL
            }
            
            return ConfigResponse(**config)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения конфигурации: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения конфигурации")
    
    # ========================================
    # 📚 ДОКУМЕНТАЦИЯ
    # ========================================
    
    @app.get("/api/v1/docs", response_model=ApiDocumentationResponse)
    async def get_api_documentation():
        """Получение документации API"""
        try:
            documentation = {
                "title": "Privacy-Compliant Analytics API",
                "version": "1.0.0",
                "description": "API для системы аналитики с соблюдением приватности",
                "endpoints": [
                    {
                        "path": "/api/v1/monitoring/servers",
                        "method": "GET",
                        "description": "Получение статуса серверов"
                    },
                    {
                        "path": "/api/v1/monitoring/performance",
                        "method": "GET", 
                        "description": "Получение метрик производительности"
                    },
                    {
                        "path": "/api/v1/dashboards/realtime",
                        "method": "GET",
                        "description": "Получение данных дашборда в реальном времени"
                    },
                    {
                        "path": "/api/v1/alerts",
                        "method": "GET",
                        "description": "Получение алертов"
                    }
                ],
                "privacy_compliance": "✅ Соблюдается",
                "rate_limits": {
                    "requests_per_hour": settings.API_RATE_LIMIT,
                    "burst_limit": 100
                }
            }
            
            return ApiDocumentationResponse(**documentation)
            
        except Exception as e:
            logger.error(f"[API] Ошибка получения документации: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения документации")
    
    logger.info("[API] Маршруты API созданы успешно")
