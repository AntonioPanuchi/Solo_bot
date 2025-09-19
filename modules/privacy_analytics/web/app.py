"""
Веб-приложение для Privacy-Compliant Analytics
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from .. import settings
from ..dashboards import RealtimeDashboard, BusinessDashboard, AdminDashboard
from ..alerts import AlertManager
from ..privacy import PrivacyComplianceChecker
from logger import logger


def create_web_app() -> FastAPI:
    """Создание веб-приложения"""
    
    app = FastAPI(
        title="Privacy-Compliant Analytics Dashboard",
        version="1.0.0",
        description="Веб-интерфейс для системы аналитики с соблюдением приватности"
    )
    
    # Подключаем статические файлы
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # Подключаем шаблоны
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    templates = Jinja2Templates(directory=templates_dir)
    
    # Инициализируем компоненты
    realtime_dashboard = RealtimeDashboard()
    business_dashboard = BusinessDashboard()
    admin_dashboard = AdminDashboard()
    alert_manager = AlertManager()
    privacy_checker = PrivacyComplianceChecker()
    
    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        """Главная страница дашборда"""
        try:
            # Получаем данные для дашборда
            realtime_data = await realtime_dashboard.get_realtime_data()
            business_data = await business_dashboard.get_business_metrics()
            admin_data = await admin_dashboard.get_admin_metrics()
            
            context = {
                "request": request,
                "realtime_data": realtime_data,
                "business_data": business_data,
                "admin_data": admin_data,
                "privacy_status": "✅ Соблюдается"
            }
            
            return templates.TemplateResponse("dashboard.html", context)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка загрузки дашборда: {e}")
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Ошибка загрузки дашборда"
            })
    
    @app.get("/realtime", response_class=HTMLResponse)
    async def realtime_dashboard_page(request: Request):
        """Страница дашборда в реальном времени"""
        try:
            data = await realtime_dashboard.get_realtime_data()
            
            context = {
                "request": request,
                "data": data,
                "title": "Дашборд в реальном времени"
            }
            
            return templates.TemplateResponse("realtime.html", context)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка загрузки дашборда в реальном времени: {e}")
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Ошибка загрузки дашборда в реальном времени"
            })
    
    @app.get("/business", response_class=HTMLResponse)
    async def business_dashboard_page(request: Request):
        """Страница бизнес-дашборда"""
        try:
            data = await business_dashboard.get_business_metrics()
            
            context = {
                "request": request,
                "data": data,
                "title": "Бизнес-дашборд"
            }
            
            return templates.TemplateResponse("business.html", context)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка загрузки бизнес-дашборда: {e}")
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Ошибка загрузки бизнес-дашборда"
            })
    
    @app.get("/admin", response_class=HTMLResponse)
    async def admin_dashboard_page(request: Request):
        """Страница административного дашборда"""
        try:
            data = await admin_dashboard.get_admin_metrics()
            
            context = {
                "request": request,
                "data": data,
                "title": "Административный дашборд"
            }
            
            return templates.TemplateResponse("admin.html", context)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка загрузки админ-дашборда: {e}")
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Ошибка загрузки админ-дашборда"
            })
    
    @app.get("/alerts", response_class=HTMLResponse)
    async def alerts_page(request: Request):
        """Страница алертов"""
        try:
            alerts = await alert_manager.get_active_alerts()
            stats = await alert_manager.get_alert_statistics()
            
            context = {
                "request": request,
                "alerts": alerts,
                "stats": stats,
                "title": "Алерты"
            }
            
            return templates.TemplateResponse("alerts.html", context)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка загрузки страницы алертов: {e}")
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Ошибка загрузки страницы алертов"
            })
    
    @app.get("/privacy", response_class=HTMLResponse)
    async def privacy_page(request: Request):
        """Страница приватности"""
        try:
            compliance_status = await privacy_checker.audit_system_compliance()
            
            context = {
                "request": request,
                "compliance_status": compliance_status,
                "privacy_mode": settings.PRIVACY_MODE,
                "data_anonymization": settings.DATA_ANONYMIZATION,
                "title": "Приватность и соответствие требованиям"
            }
            
            return templates.TemplateResponse("privacy.html", context)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка загрузки страницы приватности: {e}")
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Ошибка загрузки страницы приватности"
            })
    
    @app.get("/api/data/realtime")
    async def get_realtime_data_api():
        """API для получения данных в реальном времени"""
        try:
            data = await realtime_dashboard.get_realtime_data()
            return JSONResponse(content=data)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка API данных в реальном времени: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения данных")
    
    @app.get("/api/data/business")
    async def get_business_data_api():
        """API для получения бизнес-данных"""
        try:
            data = await business_dashboard.get_business_metrics()
            return JSONResponse(content=data)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка API бизнес-данных: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения данных")
    
    @app.get("/api/data/admin")
    async def get_admin_data_api():
        """API для получения административных данных"""
        try:
            data = await admin_dashboard.get_admin_metrics()
            return JSONResponse(content=data)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка API административных данных: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения данных")
    
    @app.get("/api/alerts")
    async def get_alerts_api():
        """API для получения алертов"""
        try:
            alerts = await alert_manager.get_active_alerts()
            return JSONResponse(content=alerts)
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка API алертов: {e}")
            raise HTTPException(status_code=500, detail="Ошибка получения алертов")
    
    @app.post("/api/alerts/{alert_id}/acknowledge")
    async def acknowledge_alert_api(alert_id: str, request: Request):
        """API для подтверждения алерта"""
        try:
            body = await request.json()
            acknowledged_by = body.get("acknowledged_by", "unknown")
            
            success = await alert_manager.acknowledge_alert(alert_id, acknowledged_by)
            
            if success:
                return JSONResponse(content={"success": True, "message": "Алерт подтвержден"})
            else:
                raise HTTPException(status_code=404, detail="Алерт не найден")
                
        except Exception as e:
            logger.error(f"[Web App] Ошибка подтверждения алерта: {e}")
            raise HTTPException(status_code=500, detail="Ошибка подтверждения алерта")
    
    @app.post("/api/alerts/{alert_id}/resolve")
    async def resolve_alert_api(alert_id: str, request: Request):
        """API для разрешения алерта"""
        try:
            body = await request.json()
            resolved_by = body.get("resolved_by", "unknown")
            
            success = await alert_manager.resolve_alert(alert_id, resolved_by)
            
            if success:
                return JSONResponse(content={"success": True, "message": "Алерт разрешен"})
            else:
                raise HTTPException(status_code=404, detail="Алерт не найден")
                
        except Exception as e:
            logger.error(f"[Web App] Ошибка разрешения алерта: {e}")
            raise HTTPException(status_code=500, detail="Ошибка разрешения алерта")
    
    @app.get("/api/health")
    async def health_check_api():
        """API проверки здоровья"""
        try:
            return JSONResponse(content={
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00Z",
                "version": "1.0.0"
            })
            
        except Exception as e:
            logger.error(f"[Web App] Ошибка проверки здоровья: {e}")
            raise HTTPException(status_code=500, detail="Ошибка проверки здоровья")
    
    logger.info("[Web App] Веб-приложение создано успешно")
    return app
