"""
Мониторинг производительности приложения
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import psutil
import aiohttp

from .. import settings
from ..privacy import PrivacyComplianceChecker
from logger import logger


class PerformanceMonitor:
    """Мониторинг производительности приложения"""
    
    def __init__(self):
        self.privacy_checker = PrivacyComplianceChecker()
        self.performance_cache = {}
        self.request_times = []
        self.error_counts = {}
        
    async def collect_performance_metrics(self):
        """Сбор метрик производительности"""
        try:
            # Собираем метрики приложения
            app_metrics = await self.get_application_metrics()
            
            # Собираем бизнес-метрики
            business_metrics = await self.get_business_metrics()
            
            # Собираем метрики здоровья системы
            health_metrics = await self.get_system_health_metrics()
            
            # Объединяем все метрики
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "application_metrics": app_metrics,
                "business_metrics": business_metrics,
                "system_health": health_metrics
            }
            
            # Проверяем соответствие требованиям приватности
            if not self.privacy_checker.validate_metrics(metrics):
                logger.warning("[Performance Monitor] Метрики не прошли проверку приватности")
                return
            
            # Сохраняем метрики
            await self.store_performance_metrics(metrics)
            
            # Кэшируем для быстрого доступа
            self.performance_cache = {
                "data": metrics,
                "timestamp": datetime.utcnow()
            }
            
            logger.debug("[Performance Monitor] Метрики производительности собраны успешно")
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка сбора метрик производительности: {e}")
    
    async def get_application_metrics(self) -> Dict[str, Any]:
        """Получение метрик приложения"""
        try:
            # Время отклика
            avg_response_time = await self.calculate_avg_response_time()
            
            # Количество запросов в секунду
            rps = await self.calculate_rps()
            
            # Процент ошибок
            error_rate = await self.calculate_error_rate()
            
            # Активные пользователи (анонимизированно)
            active_users = await self.get_active_users_count()
            
            # Подключения к базе данных
            db_connections = await self.get_database_connections()
            
            # Использование памяти приложением
            memory_usage = await self.get_application_memory_usage()
            
            return {
                "response_time_ms": avg_response_time,
                "requests_per_second": rps,
                "error_rate_percent": error_rate,
                "active_users": active_users,
                "database_connections": db_connections,
                "memory_usage_mb": memory_usage,
                "uptime_hours": await self.get_application_uptime()
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения метрик приложения: {e}")
            return {}
    
    async def get_business_metrics(self) -> Dict[str, Any]:
        """Получение бизнес-метрик"""
        try:
            # Регистрации (анонимизированно)
            registrations_rate = await self.get_registrations_rate()
            
            # Успешность платежей
            payment_success_rate = await self.get_payment_success_rate()
            
            # Продление подписок
            renewal_rate = await self.get_renewal_rate()
            
            # Удержание пользователей
            retention_rate = await self.get_retention_rate()
            
            # Конверсия
            conversion_rate = await self.get_conversion_rate()
            
            return {
                "new_registrations_per_hour": registrations_rate,
                "payment_success_rate_percent": payment_success_rate,
                "subscription_renewal_rate_percent": renewal_rate,
                "user_retention_rate_percent": retention_rate,
                "conversion_rate_percent": conversion_rate,
                "revenue_today": await self.get_daily_revenue()
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения бизнес-метрик: {e}")
            return {}
    
    async def get_system_health_metrics(self) -> Dict[str, Any]:
        """Получение метрик здоровья системы"""
        try:
            # Здоровье базы данных
            db_health = await self.check_database_health()
            
            # Здоровье Redis
            redis_health = await self.check_redis_health()
            
            # Здоровье внешних API
            external_apis_health = await self.check_external_apis_health()
            
            # Общий индекс здоровья
            overall_health = await self.calculate_overall_health_score()
            
            return {
                "database_health": db_health,
                "redis_health": redis_health,
                "external_apis_health": external_apis_health,
                "overall_health_score": overall_health,
                "system_load": await self.get_system_load(),
                "disk_io": await self.get_disk_io_stats()
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения метрик здоровья: {e}")
            return {}
    
    async def calculate_avg_response_time(self) -> float:
        """Расчет среднего времени отклика"""
        try:
            if not self.request_times:
                return 0.0
            
            # Удаляем старые записи (старше 1 часа)
            cutoff_time = time.time() - 3600
            self.request_times = [t for t in self.request_times if t > cutoff_time]
            
            if not self.request_times:
                return 0.0
            
            return round(sum(self.request_times) / len(self.request_times) * 1000, 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка расчета времени отклика: {e}")
            return 0.0
    
    async def calculate_rps(self) -> float:
        """Расчет запросов в секунду"""
        try:
            # Считаем запросы за последнюю минуту
            cutoff_time = time.time() - 60
            recent_requests = [t for t in self.request_times if t > cutoff_time]
            
            return round(len(recent_requests) / 60, 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка расчета RPS: {e}")
            return 0.0
    
    async def calculate_error_rate(self) -> float:
        """Расчет процента ошибок"""
        try:
            total_requests = len(self.request_times)
            if total_requests == 0:
                return 0.0
            
            total_errors = sum(self.error_counts.values())
            error_rate = (total_errors / total_requests) * 100
            
            return round(error_rate, 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка расчета процента ошибок: {e}")
            return 0.0
    
    async def get_active_users_count(self) -> int:
        """Получение количества активных пользователей (анонимизированно)"""
        try:
            # Здесь должна быть логика получения из базы данных
            # Возвращаем случайное число для примера
            import random
            return random.randint(100, 500)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения активных пользователей: {e}")
            return 0
    
    async def get_database_connections(self) -> int:
        """Получение количества подключений к БД"""
        try:
            # Здесь должна быть логика получения из пула подключений
            import random
            return random.randint(5, 20)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения подключений к БД: {e}")
            return 0
    
    async def get_application_memory_usage(self) -> float:
        """Получение использования памяти приложением"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            return round(memory_info.rss / (1024 * 1024), 2)  # MB
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения использования памяти: {e}")
            return 0.0
    
    async def get_application_uptime(self) -> float:
        """Получение времени работы приложения"""
        try:
            process = psutil.Process()
            uptime_seconds = time.time() - process.create_time()
            return round(uptime_seconds / 3600, 2)  # часы
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения времени работы: {e}")
            return 0.0
    
    async def get_registrations_rate(self) -> int:
        """Получение количества регистраций в час"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return random.randint(5, 25)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения регистраций: {e}")
            return 0
    
    async def get_payment_success_rate(self) -> float:
        """Получение процента успешных платежей"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return round(random.uniform(95, 99), 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения успешности платежей: {e}")
            return 0.0
    
    async def get_renewal_rate(self) -> float:
        """Получение процента продления подписок"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return round(random.uniform(70, 85), 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения продлений: {e}")
            return 0.0
    
    async def get_retention_rate(self) -> float:
        """Получение процента удержания пользователей"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return round(random.uniform(80, 95), 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения удержания: {e}")
            return 0.0
    
    async def get_conversion_rate(self) -> float:
        """Получение процента конверсии"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return round(random.uniform(2, 8), 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения конверсии: {e}")
            return 0.0
    
    async def get_daily_revenue(self) -> float:
        """Получение дневной выручки"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return round(random.uniform(50000, 150000), 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения выручки: {e}")
            return 0.0
    
    async def check_database_health(self) -> Dict[str, Any]:
        """Проверка здоровья базы данных"""
        try:
            # Здесь должна быть логика проверки БД
            return {
                "status": "healthy",
                "response_time_ms": 15.5,
                "connections_active": 8,
                "connections_max": 20
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка проверки БД: {e}")
            return {"status": "error"}
    
    async def check_redis_health(self) -> Dict[str, Any]:
        """Проверка здоровья Redis"""
        try:
            # Здесь должна быть логика проверки Redis
            return {
                "status": "healthy",
                "response_time_ms": 2.1,
                "memory_usage_percent": 45.2,
                "keys_count": 1250
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка проверки Redis: {e}")
            return {"status": "error"}
    
    async def check_external_apis_health(self) -> Dict[str, Any]:
        """Проверка здоровья внешних API"""
        try:
            # Здесь должна быть логика проверки внешних API
            return {
                "payment_apis": "healthy",
                "telegram_api": "healthy",
                "monitoring_apis": "healthy",
                "overall_status": "healthy"
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка проверки внешних API: {e}")
            return {"overall_status": "error"}
    
    async def calculate_overall_health_score(self) -> float:
        """Расчет общего индекса здоровья системы"""
        try:
            # Получаем метрики здоровья
            db_health = await self.check_database_health()
            redis_health = await self.check_redis_health()
            external_apis = await self.check_external_apis_health()
            
            # Рассчитываем индекс (0-100)
            scores = []
            
            if db_health.get("status") == "healthy":
                scores.append(100)
            else:
                scores.append(0)
            
            if redis_health.get("status") == "healthy":
                scores.append(100)
            else:
                scores.append(0)
            
            if external_apis.get("overall_status") == "healthy":
                scores.append(100)
            else:
                scores.append(0)
            
            # Добавляем метрики производительности
            error_rate = await self.calculate_error_rate()
            scores.append(max(0, 100 - error_rate * 10))
            
            response_time = await self.calculate_avg_response_time()
            scores.append(max(0, 100 - (response_time / 10)))
            
            # Средневзвешенный индекс
            overall_score = sum(scores) / len(scores)
            return round(overall_score, 2)
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка расчета индекса здоровья: {e}")
            return 0.0
    
    async def get_system_load(self) -> Dict[str, float]:
        """Получение загрузки системы"""
        try:
            load_avg = psutil.getloadavg()
            return {
                "1min": round(load_avg[0], 2),
                "5min": round(load_avg[1], 2),
                "15min": round(load_avg[2], 2)
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения загрузки системы: {e}")
            return {}
    
    async def get_disk_io_stats(self) -> Dict[str, Any]:
        """Получение статистики дискового ввода-вывода"""
        try:
            disk_io = psutil.disk_io_counters()
            return {
                "read_bytes": disk_io.read_bytes,
                "write_bytes": disk_io.write_bytes,
                "read_count": disk_io.read_count,
                "write_count": disk_io.write_count
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения статистики диска: {e}")
            return {}
    
    async def store_performance_metrics(self, metrics: Dict[str, Any]):
        """Сохранение метрик производительности"""
        try:
            # Здесь должна быть логика сохранения в базу данных
            logger.debug("[Performance Monitor] Сохранение метрик производительности")
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка сохранения метрик: {e}")
    
    def record_request_time(self, request_time: float):
        """Запись времени выполнения запроса"""
        try:
            self.request_times.append(request_time)
            
            # Ограничиваем размер списка
            if len(self.request_times) > 10000:
                self.request_times = self.request_times[-5000:]
                
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка записи времени запроса: {e}")
    
    def record_error(self, error_type: str):
        """Запись ошибки"""
        try:
            if error_type not in self.error_counts:
                self.error_counts[error_type] = 0
            self.error_counts[error_type] += 1
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка записи ошибки: {e}")
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Получение сводки по производительности"""
        try:
            if not self.performance_cache:
                return {"status": "no_data"}
            
            metrics = self.performance_cache["data"]
            
            return {
                "status": "ok",
                "last_update": metrics["timestamp"],
                "response_time_ms": metrics.get("application_metrics", {}).get("response_time_ms", 0),
                "rps": metrics.get("application_metrics", {}).get("requests_per_second", 0),
                "error_rate": metrics.get("application_metrics", {}).get("error_rate_percent", 0),
                "health_score": metrics.get("system_health", {}).get("overall_health_score", 0),
                "active_users": metrics.get("application_metrics", {}).get("active_users", 0)
            }
            
        except Exception as e:
            logger.error(f"[Performance Monitor] Ошибка получения сводки: {e}")
            return {"status": "error"}
