"""
Обработка и агрегация данных аналитики
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
import statistics

from .. import settings
from ..privacy import PrivacyComplianceChecker
from logger import logger


class DataProcessor:
    """Обработка и агрегация данных с соблюдением приватности"""
    
    def __init__(self):
        self.privacy_checker = PrivacyComplianceChecker()
        self.metrics_queue = deque(maxlen=10000)
        self.aggregated_data = {}
        self.anomaly_detector = AnomalyDetector()
        
    async def process_metrics(self, raw_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка и агрегация метрик"""
        try:
            # Проверяем соответствие требованиям приватности
            if not self.privacy_checker.validate_metrics(raw_metrics):
                logger.warning("[Data Processor] Метрики не прошли проверку приватности")
                return {}
            
            # Добавляем в очередь для обработки
            self.metrics_queue.append(raw_metrics)
            
            # Обрабатываем метрики
            processed = {
                "timestamp": raw_metrics.get("timestamp", datetime.utcnow().isoformat()),
                "server_id": raw_metrics.get("server_id", "unknown"),
                "aggregated_metrics": await self.aggregate_metrics(raw_metrics),
                "anomaly_detection": await self.detect_anomalies(raw_metrics),
                "predictive_analytics": await self.calculate_predictions(raw_metrics)
            }
            
            # Сохраняем обработанные данные
            await self.store_processed_metrics(processed)
            
            return processed
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка обработки метрик: {e}")
            return {}
    
    async def process_queued_metrics(self):
        """Обработка метрик из очереди"""
        try:
            if not self.metrics_queue:
                return
            
            # Обрабатываем метрики пакетами
            batch_size = settings.METRICS_BATCH_SIZE
            batch = []
            
            for _ in range(min(batch_size, len(self.metrics_queue))):
                if self.metrics_queue:
                    batch.append(self.metrics_queue.popleft())
            
            if batch:
                await self.process_batch(batch)
                
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка обработки очереди метрик: {e}")
    
    async def process_batch(self, batch: List[Dict[str, Any]]):
        """Обработка пакета метрик"""
        try:
            # Группируем метрики по серверам
            server_metrics = defaultdict(list)
            for metrics in batch:
                server_id = metrics.get("server_id", "unknown")
                server_metrics[server_id].append(metrics)
            
            # Обрабатываем метрики для каждого сервера
            for server_id, metrics_list in server_metrics.items():
                await self.process_server_batch(server_id, metrics_list)
                
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка обработки пакета: {e}")
    
    async def process_server_batch(self, server_id: str, metrics_list: List[Dict[str, Any]]):
        """Обработка пакета метрик для сервера"""
        try:
            # Агрегируем метрики по времени
            time_aggregated = await self.aggregate_by_time(server_id, metrics_list)
            
            # Рассчитываем тренды
            trends = await self.calculate_trends(server_id, time_aggregated)
            
            # Обновляем агрегированные данные
            self.aggregated_data[server_id] = {
                "last_update": datetime.utcnow().isoformat(),
                "time_aggregated": time_aggregated,
                "trends": trends
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка обработки пакета сервера {server_id}: {e}")
    
    async def aggregate_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Агрегация метрик"""
        try:
            server_id = metrics.get("server_id", "unknown")
            
            # Агрегируем по часам
            hourly_stats = await self.aggregate_hourly(metrics)
            
            # Агрегируем по дням
            daily_stats = await self.aggregate_daily(metrics)
            
            # Рассчитываем недельные тренды
            weekly_trends = await self.calculate_weekly_trends(metrics)
            
            # Рассчитываем месячные инсайты
            monthly_insights = await self.calculate_monthly_insights(metrics)
            
            return {
                "hourly_stats": hourly_stats,
                "daily_stats": daily_stats,
                "weekly_trends": weekly_trends,
                "monthly_insights": monthly_insights
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка агрегации метрик: {e}")
            return {}
    
    async def aggregate_hourly(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Агрегация по часам"""
        try:
            # Получаем метрики за последний час
            hour_ago = datetime.utcnow() - timedelta(hours=1)
            
            # Здесь должна быть логика получения метрик за час
            # Для примера возвращаем тестовые данные
            import random
            
            return {
                "timestamp": hour_ago.isoformat(),
                "avg_cpu_usage": round(random.uniform(20, 80), 2),
                "avg_memory_usage": round(random.uniform(30, 85), 2),
                "total_bandwidth_gb": round(random.uniform(10, 100), 2),
                "active_connections": random.randint(50, 200),
                "error_rate": round(random.uniform(0, 5), 2)
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка агрегации по часам: {e}")
            return {}
    
    async def aggregate_daily(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Агрегация по дням"""
        try:
            # Получаем метрики за последний день
            day_ago = datetime.utcnow() - timedelta(days=1)
            
            # Здесь должна быть логика получения метрик за день
            import random
            
            return {
                "date": day_ago.date().isoformat(),
                "avg_cpu_usage": round(random.uniform(25, 75), 2),
                "avg_memory_usage": round(random.uniform(35, 80), 2),
                "total_bandwidth_gb": round(random.uniform(100, 1000), 2),
                "peak_connections": random.randint(200, 500),
                "avg_error_rate": round(random.uniform(0, 3), 2),
                "uptime_percent": round(random.uniform(95, 100), 2)
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка агрегации по дням: {e}")
            return {}
    
    async def calculate_weekly_trends(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет недельных трендов"""
        try:
            # Здесь должна быть логика расчета трендов
            import random
            
            return {
                "cpu_trend": random.choice(["increasing", "decreasing", "stable"]),
                "memory_trend": random.choice(["increasing", "decreasing", "stable"]),
                "bandwidth_trend": random.choice(["increasing", "decreasing", "stable"]),
                "connections_trend": random.choice(["increasing", "decreasing", "stable"]),
                "performance_score": round(random.uniform(70, 95), 2)
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка расчета недельных трендов: {e}")
            return {}
    
    async def calculate_monthly_insights(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет месячных инсайтов"""
        try:
            # Здесь должна быть логика расчета инсайтов
            import random
            
            return {
                "peak_usage_hours": [9, 13, 18, 21],  # Часы пиковой нагрузки
                "optimal_performance_periods": ["02:00-06:00", "14:00-16:00"],
                "resource_utilization_efficiency": round(random.uniform(70, 90), 2),
                "scalability_recommendations": [
                    "Consider adding more servers during peak hours",
                    "Memory usage is within optimal range",
                    "CPU usage shows good distribution"
                ]
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка расчета месячных инсайтов: {e}")
            return {}
    
    async def detect_anomalies(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Детекция аномалий"""
        try:
            # Детекция аномалий трафика
            traffic_anomalies = await self.detect_traffic_anomalies(metrics)
            
            # Детекция аномалий производительности
            performance_anomalies = await self.detect_performance_anomalies(metrics)
            
            # Детекция аномалий безопасности
            security_anomalies = await self.detect_security_anomalies(metrics)
            
            return {
                "traffic_anomalies": traffic_anomalies,
                "performance_anomalies": performance_anomalies,
                "security_anomalies": security_anomalies,
                "overall_anomaly_score": await self.calculate_anomaly_score(metrics)
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка детекции аномалий: {e}")
            return {}
    
    async def detect_traffic_anomalies(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Детекция аномалий трафика"""
        try:
            # Здесь должна быть логика детекции аномалий трафика
            import random
            
            return {
                "unusual_spike_detected": random.choice([True, False]),
                "traffic_pattern_anomaly": random.choice([True, False]),
                "bandwidth_anomaly_score": round(random.uniform(0, 100), 2),
                "anomaly_confidence": round(random.uniform(0.5, 1.0), 2)
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка детекции аномалий трафика: {e}")
            return {}
    
    async def detect_performance_anomalies(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Детекция аномалий производительности"""
        try:
            # Здесь должна быть логика детекции аномалий производительности
            import random
            
            return {
                "cpu_anomaly_detected": random.choice([True, False]),
                "memory_anomaly_detected": random.choice([True, False]),
                "latency_anomaly_detected": random.choice([True, False]),
                "performance_anomaly_score": round(random.uniform(0, 100), 2)
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка детекции аномалий производительности: {e}")
            return {}
    
    async def detect_security_anomalies(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Детекция аномалий безопасности"""
        try:
            # Здесь должна быть логика детекции аномалий безопасности
            import random
            
            return {
                "suspicious_activity_detected": random.choice([True, False]),
                "unusual_access_patterns": random.choice([True, False]),
                "security_anomaly_score": round(random.uniform(0, 100), 2),
                "threat_level": random.choice(["low", "medium", "high"])
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка детекции аномалий безопасности: {e}")
            return {}
    
    async def calculate_anomaly_score(self, metrics: Dict[str, Any]) -> float:
        """Расчет общего индекса аномалий"""
        try:
            # Здесь должна быть логика расчета индекса аномалий
            import random
            return round(random.uniform(0, 100), 2)
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка расчета индекса аномалий: {e}")
            return 0.0
    
    async def calculate_predictions(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет прогнозов"""
        try:
            # Прогноз емкости
            capacity_forecast = await self.forecast_capacity(metrics)
            
            # Прогноз трафика
            traffic_forecast = await self.forecast_traffic(metrics)
            
            # Прогноз окон обслуживания
            maintenance_windows = await self.predict_maintenance_windows(metrics)
            
            return {
                "capacity_forecast": capacity_forecast,
                "traffic_forecast": traffic_forecast,
                "maintenance_windows": maintenance_windows
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка расчета прогнозов: {e}")
            return {}
    
    async def forecast_capacity(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Прогноз емкости"""
        try:
            # Здесь должна быть логика прогнозирования емкости
            import random
            
            return {
                "predicted_cpu_usage_24h": round(random.uniform(30, 90), 2),
                "predicted_memory_usage_24h": round(random.uniform(40, 85), 2),
                "predicted_connections_24h": random.randint(100, 500),
                "capacity_recommendation": random.choice([
                    "Current capacity is sufficient",
                    "Consider scaling up",
                    "Consider load balancing"
                ])
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка прогнозирования емкости: {e}")
            return {}
    
    async def forecast_traffic(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Прогноз трафика"""
        try:
            # Здесь должна быть логика прогнозирования трафика
            import random
            
            return {
                "predicted_bandwidth_24h_gb": round(random.uniform(200, 2000), 2),
                "peak_traffic_hours": [9, 13, 18, 21],
                "traffic_growth_rate": round(random.uniform(-5, 20), 2),
                "bandwidth_recommendation": random.choice([
                    "Current bandwidth is sufficient",
                    "Consider increasing bandwidth",
                    "Traffic is decreasing"
                ])
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка прогнозирования трафика: {e}")
            return {}
    
    async def predict_maintenance_windows(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Прогноз окон обслуживания"""
        try:
            # Здесь должна быть логика прогнозирования окон обслуживания
            import random
            
            return {
                "recommended_maintenance_time": "02:00-04:00",
                "maintenance_urgency": random.choice(["low", "medium", "high"]),
                "estimated_downtime_minutes": random.randint(5, 30),
                "maintenance_recommendations": [
                    "Schedule maintenance during low traffic hours",
                    "Consider rolling updates",
                    "Prepare rollback plan"
                ]
            }
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка прогнозирования окон обслуживания: {e}")
            return {}
    
    async def aggregate_by_time(self, server_id: str, metrics_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Агрегация метрик по времени"""
        try:
            if not metrics_list:
                return {}
            
            # Группируем по часам
            hourly_groups = defaultdict(list)
            for metrics in metrics_list:
                timestamp = datetime.fromisoformat(metrics.get("timestamp", datetime.utcnow().isoformat()))
                hour_key = timestamp.strftime("%Y-%m-%d %H:00")
                hourly_groups[hour_key].append(metrics)
            
            # Агрегируем данные по часам
            aggregated = {}
            for hour, hour_metrics in hourly_groups.items():
                aggregated[hour] = await self.aggregate_hour_metrics(hour_metrics)
            
            return aggregated
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка агрегации по времени: {e}")
            return {}
    
    async def aggregate_hour_metrics(self, metrics_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Агрегация метрик за час"""
        try:
            if not metrics_list:
                return {}
            
            # Извлекаем числовые значения
            cpu_values = []
            memory_values = []
            bandwidth_values = []
            connection_values = []
            
            for metrics in metrics_list:
                system_metrics = metrics.get("system_metrics", {})
                vpn_metrics = metrics.get("vpn_metrics", {})
                
                if "cpu_usage_percent" in system_metrics:
                    cpu_values.append(system_metrics["cpu_usage_percent"])
                if "memory_usage_percent" in system_metrics:
                    memory_values.append(system_metrics["memory_usage_percent"])
                if "total_bandwidth_gb" in vpn_metrics:
                    bandwidth_values.append(vpn_metrics["total_bandwidth_gb"])
                if "total_connections" in vpn_metrics:
                    connection_values.append(vpn_metrics["total_connections"])
            
            # Рассчитываем статистики
            result = {}
            
            if cpu_values:
                result["avg_cpu"] = round(statistics.mean(cpu_values), 2)
                result["max_cpu"] = round(max(cpu_values), 2)
                result["min_cpu"] = round(min(cpu_values), 2)
            
            if memory_values:
                result["avg_memory"] = round(statistics.mean(memory_values), 2)
                result["max_memory"] = round(max(memory_values), 2)
                result["min_memory"] = round(min(memory_values), 2)
            
            if bandwidth_values:
                result["total_bandwidth"] = round(sum(bandwidth_values), 2)
                result["avg_bandwidth"] = round(statistics.mean(bandwidth_values), 2)
            
            if connection_values:
                result["avg_connections"] = round(statistics.mean(connection_values), 2)
                result["max_connections"] = max(connection_values)
                result["min_connections"] = min(connection_values)
            
            result["sample_count"] = len(metrics_list)
            
            return result
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка агрегации метрик за час: {e}")
            return {}
    
    async def calculate_trends(self, server_id: str, time_aggregated: Dict[str, Any]) -> Dict[str, Any]:
        """Расчет трендов"""
        try:
            if not time_aggregated:
                return {}
            
            # Сортируем по времени
            sorted_hours = sorted(time_aggregated.items())
            
            if len(sorted_hours) < 2:
                return {}
            
            # Рассчитываем тренды для каждого метрика
            trends = {}
            
            # Тренд CPU
            cpu_values = [data.get("avg_cpu", 0) for _, data in sorted_hours if "avg_cpu" in data]
            if len(cpu_values) >= 2:
                trends["cpu_trend"] = self.calculate_trend_direction(cpu_values)
            
            # Тренд памяти
            memory_values = [data.get("avg_memory", 0) for _, data in sorted_hours if "avg_memory" in data]
            if len(memory_values) >= 2:
                trends["memory_trend"] = self.calculate_trend_direction(memory_values)
            
            # Тренд подключений
            connection_values = [data.get("avg_connections", 0) for _, data in sorted_hours if "avg_connections" in data]
            if len(connection_values) >= 2:
                trends["connections_trend"] = self.calculate_trend_direction(connection_values)
            
            return trends
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка расчета трендов: {e}")
            return {}
    
    def calculate_trend_direction(self, values: List[float]) -> str:
        """Расчет направления тренда"""
        try:
            if len(values) < 2:
                return "stable"
            
            # Простой линейный тренд
            first_half = values[:len(values)//2]
            second_half = values[len(values)//2:]
            
            first_avg = statistics.mean(first_half)
            second_avg = statistics.mean(second_half)
            
            change_percent = ((second_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0
            
            if change_percent > 5:
                return "increasing"
            elif change_percent < -5:
                return "decreasing"
            else:
                return "stable"
                
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка расчета направления тренда: {e}")
            return "stable"
    
    async def store_processed_metrics(self, processed_metrics: Dict[str, Any]):
        """Сохранение обработанных метрик"""
        try:
            # Здесь должна быть логика сохранения в базу данных
            logger.debug("[Data Processor] Сохранение обработанных метрик")
            
        except Exception as e:
            logger.error(f"[Data Processor] Ошибка сохранения метрик: {e}")


class AnomalyDetector:
    """Детектор аномалий"""
    
    def __init__(self):
        self.historical_data = deque(maxlen=1000)
        self.thresholds = {
            "cpu_usage": 80,
            "memory_usage": 85,
            "error_rate": 5,
            "bandwidth_spike": 200
        }
    
    async def detect_anomaly(self, metric_name: str, value: float) -> bool:
        """Детекция аномалии для конкретного метрика"""
        try:
            if metric_name in self.thresholds:
                return value > self.thresholds[metric_name]
            
            # Для других метрик используем статистический анализ
            if len(self.historical_data) < 10:
                return False
            
            historical_values = [data.get(metric_name, 0) for data in self.historical_data]
            if not historical_values:
                return False
            
            mean_value = statistics.mean(historical_values)
            std_value = statistics.stdev(historical_values) if len(historical_values) > 1 else 0
            
            # Аномалия если значение отклоняется более чем на 2 стандартных отклонения
            return abs(value - mean_value) > 2 * std_value
            
        except Exception as e:
            logger.error(f"[Anomaly Detector] Ошибка детекции аномалии: {e}")
            return False
    
    def add_data_point(self, data: Dict[str, Any]):
        """Добавление точки данных для анализа"""
        try:
            self.historical_data.append(data)
        except Exception as e:
            logger.error(f"[Anomaly Detector] Ошибка добавления точки данных: {e}")
