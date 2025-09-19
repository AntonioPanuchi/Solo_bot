"""
Калькулятор метрик для аналитики
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import statistics
import math

from .. import settings
from ..privacy import PrivacyComplianceChecker
from logger import logger


class MetricsCalculator:
    """Калькулятор метрик с соблюдением приватности"""
    
    def __init__(self):
        self.privacy_checker = PrivacyComplianceChecker()
        self.cached_metrics = {}
        
    async def calculate_performance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик производительности"""
        try:
            # Проверяем соответствие требованиям приватности
            if not self.privacy_checker.validate_metrics(data):
                logger.warning("[Metrics Calculator] Данные не прошли проверку приватности")
                return {}
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "performance_score": await self.calculate_performance_score(data),
                "efficiency_metrics": await self.calculate_efficiency_metrics(data),
                "reliability_metrics": await self.calculate_reliability_metrics(data),
                "scalability_metrics": await self.calculate_scalability_metrics(data)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик производительности: {e}")
            return {}
    
    async def calculate_business_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет бизнес-метрик"""
        try:
            # Проверяем соответствие требованиям приватности
            if not self.privacy_checker.validate_metrics(data):
                logger.warning("[Metrics Calculator] Данные не прошли проверку приватности")
                return {}
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "revenue_metrics": await self.calculate_revenue_metrics(data),
                "user_metrics": await self.calculate_user_metrics(data),
                "conversion_metrics": await self.calculate_conversion_metrics(data),
                "retention_metrics": await self.calculate_retention_metrics(data)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета бизнес-метрик: {e}")
            return {}
    
    async def calculate_security_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик безопасности"""
        try:
            # Проверяем соответствие требованиям приватности
            if not self.privacy_checker.validate_metrics(data):
                logger.warning("[Metrics Calculator] Данные не прошли проверку приватности")
                return {}
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "threat_level": await self.calculate_threat_level(data),
                "security_score": await self.calculate_security_score(data),
                "compliance_metrics": await self.calculate_compliance_metrics(data),
                "incident_metrics": await self.calculate_incident_metrics(data)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик безопасности: {e}")
            return {}
    
    async def calculate_performance_score(self, data: Dict[str, Any]) -> float:
        """Расчет общего индекса производительности"""
        try:
            system_metrics = data.get("system_metrics", {})
            quality_metrics = data.get("quality_metrics", {})
            
            # Метрики системы
            cpu_usage = system_metrics.get("cpu_usage_percent", 0)
            memory_usage = system_metrics.get("memory_usage_percent", 0)
            disk_usage = system_metrics.get("disk_usage_percent", 0)
            
            # Метрики качества
            latency = quality_metrics.get("avg_latency_ms", 0)
            error_rate = quality_metrics.get("error_rate_percent", 0)
            success_rate = quality_metrics.get("success_rate_percent", 100)
            
            # Рассчитываем компоненты индекса
            cpu_score = max(0, 100 - cpu_usage)
            memory_score = max(0, 100 - memory_usage)
            disk_score = max(0, 100 - disk_usage)
            latency_score = max(0, 100 - (latency / 10))  # Нормализуем латентность
            error_score = max(0, 100 - (error_rate * 10))
            success_score = success_rate
            
            # Средневзвешенный индекс
            performance_score = (
                cpu_score * 0.2 +
                memory_score * 0.2 +
                disk_score * 0.15 +
                latency_score * 0.15 +
                error_score * 0.15 +
                success_score * 0.15
            )
            
            return round(performance_score, 2)
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета индекса производительности: {e}")
            return 0.0
    
    async def calculate_efficiency_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик эффективности"""
        try:
            system_metrics = data.get("system_metrics", {})
            vpn_metrics = data.get("vpn_metrics", {})
            
            # Использование ресурсов
            cpu_efficiency = await self.calculate_cpu_efficiency(system_metrics)
            memory_efficiency = await self.calculate_memory_efficiency(system_metrics)
            bandwidth_efficiency = await self.calculate_bandwidth_efficiency(vpn_metrics)
            
            # Общая эффективность
            overall_efficiency = (cpu_efficiency + memory_efficiency + bandwidth_efficiency) / 3
            
            return {
                "cpu_efficiency": cpu_efficiency,
                "memory_efficiency": memory_efficiency,
                "bandwidth_efficiency": bandwidth_efficiency,
                "overall_efficiency": round(overall_efficiency, 2),
                "resource_utilization": await self.calculate_resource_utilization(system_metrics)
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик эффективности: {e}")
            return {}
    
    async def calculate_reliability_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик надежности"""
        try:
            quality_metrics = data.get("quality_metrics", {})
            
            # Основные метрики надежности
            uptime = await self.calculate_uptime(data)
            error_rate = quality_metrics.get("error_rate_percent", 0)
            success_rate = quality_metrics.get("success_rate_percent", 100)
            packet_loss = quality_metrics.get("packet_loss_percent", 0)
            
            # Индекс надежности
            reliability_score = (
                uptime * 0.4 +
                success_rate * 0.3 +
                (100 - error_rate) * 0.2 +
                (100 - packet_loss) * 0.1
            )
            
            return {
                "uptime_percent": uptime,
                "error_rate_percent": error_rate,
                "success_rate_percent": success_rate,
                "packet_loss_percent": packet_loss,
                "reliability_score": round(reliability_score, 2),
                "mean_time_between_failures": await self.calculate_mtbf(data),
                "mean_time_to_recovery": await self.calculate_mttr(data)
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик надежности: {e}")
            return {}
    
    async def calculate_scalability_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик масштабируемости"""
        try:
            system_metrics = data.get("system_metrics", {})
            vpn_metrics = data.get("vpn_metrics", {})
            
            # Текущая нагрузка
            current_load = await self.calculate_current_load(system_metrics)
            
            # Потенциал масштабирования
            scaling_potential = await self.calculate_scaling_potential(system_metrics)
            
            # Рекомендации по масштабированию
            scaling_recommendations = await self.get_scaling_recommendations(system_metrics, vpn_metrics)
            
            return {
                "current_load_percent": current_load,
                "scaling_potential": scaling_potential,
                "scaling_recommendations": scaling_recommendations,
                "capacity_utilization": await self.calculate_capacity_utilization(system_metrics),
                "growth_readiness": await self.calculate_growth_readiness(data)
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик масштабируемости: {e}")
            return {}
    
    async def calculate_revenue_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик выручки"""
        try:
            # Здесь должна быть логика получения данных о выручке
            # Для примера возвращаем тестовые данные
            import random
            
            daily_revenue = random.uniform(10000, 50000)
            monthly_revenue = daily_revenue * 30
            growth_rate = random.uniform(-5, 25)
            
            return {
                "daily_revenue": round(daily_revenue, 2),
                "monthly_revenue": round(monthly_revenue, 2),
                "revenue_growth_rate": round(growth_rate, 2),
                "average_revenue_per_user": round(daily_revenue / random.randint(100, 500), 2),
                "revenue_efficiency": round(random.uniform(70, 95), 2)
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик выручки: {e}")
            return {}
    
    async def calculate_user_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик пользователей"""
        try:
            # Здесь должна быть логика получения данных о пользователях
            import random
            
            total_users = random.randint(1000, 5000)
            active_users = random.randint(200, 800)
            new_users = random.randint(5, 25)
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "new_users_today": new_users,
                "user_growth_rate": round(random.uniform(5, 25), 2),
                "user_engagement_score": round(random.uniform(60, 90), 2),
                "user_satisfaction_score": round(random.uniform(70, 95), 2)
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик пользователей: {e}")
            return {}
    
    async def calculate_conversion_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик конверсии"""
        try:
            # Здесь должна быть логика расчета конверсии
            import random
            
            return {
                "overall_conversion_rate": round(random.uniform(2, 8), 2),
                "trial_to_paid_conversion": round(random.uniform(15, 35), 2),
                "visitor_to_trial_conversion": round(random.uniform(5, 15), 2),
                "conversion_funnel_efficiency": round(random.uniform(60, 85), 2),
                "conversion_optimization_score": round(random.uniform(70, 95), 2)
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик конверсии: {e}")
            return {}
    
    async def calculate_retention_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик удержания"""
        try:
            # Здесь должна быть логика расчета удержания
            import random
            
            return {
                "retention_rate_1_day": round(random.uniform(80, 95), 2),
                "retention_rate_7_days": round(random.uniform(60, 80), 2),
                "retention_rate_30_days": round(random.uniform(40, 70), 2),
                "churn_rate": round(random.uniform(5, 15), 2),
                "lifetime_value": round(random.uniform(100, 500), 2)
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик удержания: {e}")
            return {}
    
    async def calculate_threat_level(self, data: Dict[str, Any]) -> str:
        """Расчет уровня угрозы"""
        try:
            # Здесь должна быть логика расчета уровня угрозы
            import random
            
            threat_score = random.randint(0, 100)
            
            if threat_score >= 80:
                return "critical"
            elif threat_score >= 60:
                return "high"
            elif threat_score >= 40:
                return "medium"
            else:
                return "low"
                
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета уровня угрозы: {e}")
            return "unknown"
    
    async def calculate_security_score(self, data: Dict[str, Any]) -> float:
        """Расчет индекса безопасности"""
        try:
            # Здесь должна быть логика расчета индекса безопасности
            import random
            
            return round(random.uniform(70, 95), 2)
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета индекса безопасности: {e}")
            return 0.0
    
    async def calculate_compliance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик соответствия требованиям"""
        try:
            # Здесь должна быть логика расчета соответствия
            import random
            
            return {
                "gdpr_compliance": round(random.uniform(85, 100), 2),
                "privacy_compliance": round(random.uniform(90, 100), 2),
                "security_compliance": round(random.uniform(80, 95), 2),
                "overall_compliance_score": round(random.uniform(85, 98), 2)
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик соответствия: {e}")
            return {}
    
    async def calculate_incident_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет метрик инцидентов"""
        try:
            # Здесь должна быть логика расчета инцидентов
            import random
            
            return {
                "security_incidents_today": random.randint(0, 5),
                "incidents_resolved": random.randint(0, 5),
                "average_resolution_time_hours": round(random.uniform(1, 24), 2),
                "incident_severity_distribution": {
                    "low": random.randint(0, 3),
                    "medium": random.randint(0, 2),
                    "high": random.randint(0, 1),
                    "critical": random.randint(0, 1)
                }
            }
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета метрик инцидентов: {e}")
            return {}
    
    # Вспомогательные методы
    
    async def calculate_cpu_efficiency(self, system_metrics: Dict[str, Any]) -> float:
        """Расчет эффективности CPU"""
        try:
            cpu_usage = system_metrics.get("cpu_usage_percent", 0)
            # Эффективность выше при умеренном использовании (50-70%)
            if 50 <= cpu_usage <= 70:
                return 100.0
            elif cpu_usage < 50:
                return cpu_usage * 2  # Недозагрузка
            else:
                return max(0, 100 - (cpu_usage - 70) * 2)  # Перегрузка
                
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета эффективности CPU: {e}")
            return 0.0
    
    async def calculate_memory_efficiency(self, system_metrics: Dict[str, Any]) -> float:
        """Расчет эффективности памяти"""
        try:
            memory_usage = system_metrics.get("memory_usage_percent", 0)
            # Эффективность выше при умеренном использовании (60-80%)
            if 60 <= memory_usage <= 80:
                return 100.0
            elif memory_usage < 60:
                return memory_usage * 1.67  # Недозагрузка
            else:
                return max(0, 100 - (memory_usage - 80) * 2.5)  # Перегрузка
                
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета эффективности памяти: {e}")
            return 0.0
    
    async def calculate_bandwidth_efficiency(self, vpn_metrics: Dict[str, Any]) -> float:
        """Расчет эффективности пропускной способности"""
        try:
            # Здесь должна быть логика расчета эффективности трафика
            import random
            return round(random.uniform(70, 95), 2)
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета эффективности трафика: {e}")
            return 0.0
    
    async def calculate_resource_utilization(self, system_metrics: Dict[str, Any]) -> float:
        """Расчет использования ресурсов"""
        try:
            cpu_usage = system_metrics.get("cpu_usage_percent", 0)
            memory_usage = system_metrics.get("memory_usage_percent", 0)
            disk_usage = system_metrics.get("disk_usage_percent", 0)
            
            # Среднее использование ресурсов
            return round((cpu_usage + memory_usage + disk_usage) / 3, 2)
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета использования ресурсов: {e}")
            return 0.0
    
    async def calculate_uptime(self, data: Dict[str, Any]) -> float:
        """Расчет времени работы"""
        try:
            # Здесь должна быть логика расчета uptime
            import random
            return round(random.uniform(95, 100), 2)
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета uptime: {e}")
            return 0.0
    
    async def calculate_mtbf(self, data: Dict[str, Any]) -> float:
        """Расчет среднего времени между отказами"""
        try:
            # Здесь должна быть логика расчета MTBF
            import random
            return round(random.uniform(24, 168), 2)  # часы
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета MTBF: {e}")
            return 0.0
    
    async def calculate_mttr(self, data: Dict[str, Any]) -> float:
        """Расчет среднего времени восстановления"""
        try:
            # Здесь должна быть логика расчета MTTR
            import random
            return round(random.uniform(0.5, 4), 2)  # часы
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета MTTR: {e}")
            return 0.0
    
    async def calculate_current_load(self, system_metrics: Dict[str, Any]) -> float:
        """Расчет текущей нагрузки"""
        try:
            cpu_usage = system_metrics.get("cpu_usage_percent", 0)
            memory_usage = system_metrics.get("memory_usage_percent", 0)
            
            # Средняя нагрузка
            return round((cpu_usage + memory_usage) / 2, 2)
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета текущей нагрузки: {e}")
            return 0.0
    
    async def calculate_scaling_potential(self, system_metrics: Dict[str, Any]) -> str:
        """Расчет потенциала масштабирования"""
        try:
            cpu_usage = system_metrics.get("cpu_usage_percent", 0)
            memory_usage = system_metrics.get("memory_usage_percent", 0)
            
            avg_usage = (cpu_usage + memory_usage) / 2
            
            if avg_usage < 30:
                return "low"
            elif avg_usage < 60:
                return "medium"
            elif avg_usage < 80:
                return "high"
            else:
                return "critical"
                
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета потенциала масштабирования: {e}")
            return "unknown"
    
    async def get_scaling_recommendations(self, system_metrics: Dict[str, Any], vpn_metrics: Dict[str, Any]) -> List[str]:
        """Получение рекомендаций по масштабированию"""
        try:
            recommendations = []
            
            cpu_usage = system_metrics.get("cpu_usage_percent", 0)
            memory_usage = system_metrics.get("memory_usage_percent", 0)
            connections = vpn_metrics.get("total_connections", 0)
            
            if cpu_usage > 80:
                recommendations.append("Consider CPU scaling or load balancing")
            if memory_usage > 85:
                recommendations.append("Consider memory upgrade or optimization")
            if connections > 500:
                recommendations.append("Consider adding more servers")
            
            if not recommendations:
                recommendations.append("Current capacity is sufficient")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка получения рекомендаций: {e}")
            return []
    
    async def calculate_capacity_utilization(self, system_metrics: Dict[str, Any]) -> float:
        """Расчет использования емкости"""
        try:
            cpu_usage = system_metrics.get("cpu_usage_percent", 0)
            memory_usage = system_metrics.get("memory_usage_percent", 0)
            disk_usage = system_metrics.get("disk_usage_percent", 0)
            
            # Среднее использование емкости
            return round((cpu_usage + memory_usage + disk_usage) / 3, 2)
            
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета использования емкости: {e}")
            return 0.0
    
    async def calculate_growth_readiness(self, data: Dict[str, Any]) -> str:
        """Расчет готовности к росту"""
        try:
            system_metrics = data.get("system_metrics", {})
            cpu_usage = system_metrics.get("cpu_usage_percent", 0)
            memory_usage = system_metrics.get("memory_usage_percent", 0)
            
            avg_usage = (cpu_usage + memory_usage) / 2
            
            if avg_usage < 50:
                return "ready"
            elif avg_usage < 70:
                return "prepared"
            elif avg_usage < 85:
                return "monitoring"
            else:
                return "critical"
                
        except Exception as e:
            logger.error(f"[Metrics Calculator] Ошибка расчета готовности к росту: {e}")
            return "unknown"
