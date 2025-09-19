"""
Мониторинг серверов с соблюдением приватности
"""

import asyncio
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import aiohttp
import asyncpg

from .. import settings
from ..privacy import PrivacyComplianceChecker
from logger import logger


class ServerMonitor:
    """Мониторинг серверов без нарушения приватности пользователей"""
    
    def __init__(self):
        self.privacy_checker = PrivacyComplianceChecker()
        self.metrics_cache = {}
        self.last_collection = {}
        
    async def collect_all_metrics(self):
        """Сбор метрик со всех серверов"""
        try:
            # Получаем список серверов из базы данных
            servers = await self.get_active_servers()
            
            tasks = []
            for server in servers:
                task = self.collect_server_metrics(server['id'])
                tasks.append(task)
            
            # Собираем метрики параллельно
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
                
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка сбора метрик: {e}")
    
    async def collect_server_metrics(self, server_id: str):
        """Сбор метрик конкретного сервера"""
        try:
            # Проверяем, не слишком ли часто собираем метрики
            now = datetime.utcnow()
            if (server_id in self.last_collection and 
                (now - self.last_collection[server_id]).seconds < settings.SERVER_MONITORING_INTERVAL):
                return
            
            self.last_collection[server_id] = now
            
            # Собираем системные метрики
            system_metrics = await self.get_system_metrics()
            
            # Собираем VPN-метрики (анонимизированные)
            vpn_metrics = await self.get_vpn_metrics(server_id)
            
            # Собираем метрики качества
            quality_metrics = await self.get_quality_metrics(server_id)
            
            # Объединяем все метрики
            metrics = {
                "server_id": server_id,
                "timestamp": now.isoformat(),
                "system_metrics": system_metrics,
                "vpn_metrics": vpn_metrics,
                "quality_metrics": quality_metrics
            }
            
            # Проверяем соответствие требованиям приватности
            if not await self.privacy_checker.validate_metrics(metrics):
                logger.warning(f"[Server Monitor] Метрики сервера {server_id} не прошли проверку приватности")
                return
            
            # Сохраняем метрики
            await self.store_metrics(metrics)
            
            # Кэшируем для быстрого доступа
            self.metrics_cache[server_id] = {
                "data": metrics,
                "timestamp": now
            }
            
            logger.debug(f"[Server Monitor] Метрики сервера {server_id} собраны успешно")
            
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка сбора метрик сервера {server_id}: {e}")
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Получение системных метрик сервера"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Память
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_gb = memory.available / (1024**3)
            
            # Диск
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free_gb = disk.free / (1024**3)
            
            # Сеть
            network = psutil.net_io_counters()
            network_bytes_sent = network.bytes_sent
            network_bytes_recv = network.bytes_recv
            
            # Время работы
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_hours = uptime_seconds / 3600
            
            return {
                "cpu_usage_percent": round(cpu_percent, 2),
                "cpu_count": cpu_count,
                "memory_usage_percent": round(memory_percent, 2),
                "memory_available_gb": round(memory_available_gb, 2),
                "disk_usage_percent": round(disk_percent, 2),
                "disk_free_gb": round(disk_free_gb, 2),
                "network_bytes_sent": network_bytes_sent,
                "network_bytes_recv": network_bytes_recv,
                "uptime_hours": round(uptime_hours, 2)
            }
            
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения системных метрик: {e}")
            return {}
    
    async def get_vpn_metrics(self, server_id: str) -> Dict[str, Any]:
        """Получение VPN-метрик (анонимизированных)"""
        try:
            # Получаем общую статистику без привязки к пользователям
            total_connections = await self.get_total_connections(server_id)
            total_bandwidth = await self.get_total_bandwidth(server_id)
            protocol_stats = await self.get_protocol_stats(server_id)
            geo_stats = await self.get_geo_stats(server_id)
            
            return {
                "total_connections": total_connections,
                "total_bandwidth_gb": round(total_bandwidth / (1024**3), 2),
                "protocol_distribution": protocol_stats,
                "geographic_distribution": geo_stats,
                "avg_connection_duration_minutes": await self.get_avg_connection_duration(server_id)
            }
            
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения VPN-метрик: {e}")
            return {}
    
    async def get_quality_metrics(self, server_id: str) -> Dict[str, Any]:
        """Получение метрик качества соединения"""
        try:
            # Тестируем латентность
            latency = await self.test_latency(server_id)
            
            # Получаем статистику ошибок
            error_rate = await self.get_error_rate(server_id)
            
            # Получаем статистику успешных подключений
            success_rate = await self.get_success_rate(server_id)
            
            return {
                "avg_latency_ms": latency,
                "error_rate_percent": error_rate,
                "success_rate_percent": success_rate,
                "packet_loss_percent": await self.get_packet_loss(server_id)
            }
            
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения метрик качества: {e}")
            return {}
    
    async def get_active_servers(self) -> List[Dict[str, Any]]:
        """Получение списка активных серверов"""
        try:
            # Здесь должна быть логика получения серверов из базы данных
            # Для примера возвращаем тестовые данные
            return [
                {"id": "server_1", "name": "US Server", "enabled": True},
                {"id": "server_2", "name": "EU Server", "enabled": True},
                {"id": "server_3", "name": "Asia Server", "enabled": True}
            ]
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения списка серверов: {e}")
            return []
    
    async def get_total_connections(self, server_id: str) -> int:
        """Получение общего количества подключений (анонимизированно)"""
        try:
            # Здесь должна быть логика получения из панели управления
            # Возвращаем случайное число для примера
            import random
            return random.randint(50, 200)
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения количества подключений: {e}")
            return 0
    
    async def get_total_bandwidth(self, server_id: str) -> int:
        """Получение общего трафика в байтах (анонимизированно)"""
        try:
            # Здесь должна быть логика получения из панели управления
            import random
            return random.randint(1000000000, 5000000000)  # 1-5 GB
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения трафика: {e}")
            return 0
    
    async def get_protocol_stats(self, server_id: str) -> Dict[str, int]:
        """Получение статистики по протоколам (анонимизированно)"""
        try:
            # Анонимизированная статистика протоколов
            return {
                "vless": 60,
                "vmess": 30,
                "trojan": 10
            }
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения статистики протоколов: {e}")
            return {}
    
    async def get_geo_stats(self, server_id: str) -> Dict[str, Any]:
        """Получение географической статистики (анонимизированно)"""
        try:
            # Анонимизированная географическая статистика
            return {
                "top_countries": [
                    {"country": "US", "connections": 45, "bandwidth_gb": 1200},
                    {"country": "DE", "connections": 35, "bandwidth_gb": 980},
                    {"country": "RU", "connections": 25, "bandwidth_gb": 850}
                ],
                "total_countries": 15,
                "geographic_diversity_score": 0.85
            }
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения географической статистики: {e}")
            return {}
    
    async def get_avg_connection_duration(self, server_id: str) -> float:
        """Получение средней продолжительности соединения в минутах"""
        try:
            import random
            return round(random.uniform(30, 180), 2)  # 30-180 минут
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения продолжительности соединения: {e}")
            return 0.0
    
    async def test_latency(self, server_id: str) -> float:
        """Тестирование латентности сервера"""
        try:
            # Здесь должна быть логика тестирования латентности
            import random
            return round(random.uniform(50, 300), 2)  # 50-300 мс
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка тестирования латентности: {e}")
            return 0.0
    
    async def get_error_rate(self, server_id: str) -> float:
        """Получение процента ошибок"""
        try:
            import random
            return round(random.uniform(0, 5), 2)  # 0-5%
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения процента ошибок: {e}")
            return 0.0
    
    async def get_success_rate(self, server_id: str) -> float:
        """Получение процента успешных подключений"""
        try:
            import random
            return round(random.uniform(95, 100), 2)  # 95-100%
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения процента успешных подключений: {e}")
            return 0.0
    
    async def get_packet_loss(self, server_id: str) -> float:
        """Получение процента потери пакетов"""
        try:
            import random
            return round(random.uniform(0, 2), 2)  # 0-2%
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения потери пакетов: {e}")
            return 0.0
    
    async def store_metrics(self, metrics: Dict[str, Any]):
        """Сохранение метрик в базу данных"""
        try:
            # Здесь должна быть логика сохранения в базу данных
            # Для примера просто логируем
            logger.debug(f"[Server Monitor] Сохранение метрик: {metrics['server_id']}")
            
            # В реальной реализации здесь будет:
            # await database.store_server_metrics(metrics)
            
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка сохранения метрик: {e}")
    
    async def get_server_health_score(self, server_id: str) -> float:
        """Расчет общего индекса здоровья сервера"""
        try:
            if server_id not in self.metrics_cache:
                return 0.0
            
            metrics = self.metrics_cache[server_id]["data"]
            system = metrics.get("system_metrics", {})
            quality = metrics.get("quality_metrics", {})
            
            # Рассчитываем индекс здоровья (0-100)
            cpu_score = max(0, 100 - system.get("cpu_usage_percent", 0))
            memory_score = max(0, 100 - system.get("memory_usage_percent", 0))
            disk_score = max(0, 100 - system.get("disk_usage_percent", 0))
            latency_score = max(0, 100 - (quality.get("avg_latency_ms", 0) / 10))
            error_score = max(0, 100 - quality.get("error_rate_percent", 0) * 10)
            
            # Средневзвешенный индекс
            health_score = (
                cpu_score * 0.25 +
                memory_score * 0.25 +
                disk_score * 0.2 +
                latency_score * 0.15 +
                error_score * 0.15
            )
            
            return round(health_score, 2)
            
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка расчета индекса здоровья: {e}")
            return 0.0
    
    async def get_server_summary(self, server_id: str) -> Dict[str, Any]:
        """Получение сводки по серверу"""
        try:
            if server_id not in self.metrics_cache:
                return {"status": "no_data"}
            
            metrics = self.metrics_cache[server_id]["data"]
            health_score = await self.get_server_health_score(server_id)
            
            return {
                "server_id": server_id,
                "status": "online" if health_score > 70 else "warning" if health_score > 40 else "critical",
                "health_score": health_score,
                "last_update": metrics["timestamp"],
                "active_connections": metrics.get("vpn_metrics", {}).get("total_connections", 0),
                "bandwidth_usage_gb": metrics.get("vpn_metrics", {}).get("total_bandwidth_gb", 0),
                "cpu_usage": metrics.get("system_metrics", {}).get("cpu_usage_percent", 0),
                "memory_usage": metrics.get("system_metrics", {}).get("memory_usage_percent", 0)
            }
            
        except Exception as e:
            logger.error(f"[Server Monitor] Ошибка получения сводки сервера: {e}")
            return {"status": "error"}
