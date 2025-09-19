"""
Менеджер алертов
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque

from .. import settings
from ..privacy import PrivacyComplianceChecker
from .notification_channels import NotificationChannels
from .escalation_rules import EscalationRules
from logger import logger


class AlertManager:
    """Менеджер алертов с соблюдением приватности"""
    
    def __init__(self):
        self.privacy_checker = PrivacyComplianceChecker()
        self.notification_channels = NotificationChannels()
        self.escalation_rules = EscalationRules()
        self.active_alerts = {}
        self.alert_history = deque(maxlen=10000)
        self.alert_rules = self.load_alert_rules()
        self.metrics_cache = {}
        
    def load_alert_rules(self) -> List[Dict[str, Any]]:
        """Загрузка правил алертов"""
        try:
            return [
                {
                    "id": "high_cpu_usage",
                    "name": "Высокое использование CPU",
                    "condition": "cpu_usage > 80",
                    "severity": "warning",
                    "message": "Высокое использование CPU на сервере {server_id}: {cpu_usage}%",
                    "channels": ["telegram", "email"],
                    "enabled": True,
                    "cooldown_minutes": 30
                },
                {
                    "id": "critical_cpu_usage",
                    "name": "Критическое использование CPU",
                    "condition": "cpu_usage > 95",
                    "severity": "critical",
                    "message": "КРИТИЧЕСКОЕ: Использование CPU превысило 95% на сервере {server_id}",
                    "channels": ["telegram", "email", "webhook"],
                    "enabled": True,
                    "cooldown_minutes": 5
                },
                {
                    "id": "high_memory_usage",
                    "name": "Высокое использование памяти",
                    "condition": "memory_usage > 85",
                    "severity": "warning",
                    "message": "Высокое использование памяти на сервере {server_id}: {memory_usage}%",
                    "channels": ["telegram", "email"],
                    "enabled": True,
                    "cooldown_minutes": 30
                },
                {
                    "id": "high_disk_usage",
                    "name": "Высокое использование диска",
                    "condition": "disk_usage > 90",
                    "severity": "warning",
                    "message": "Высокое использование диска на сервере {server_id}: {disk_usage}%",
                    "channels": ["telegram", "email"],
                    "enabled": True,
                    "cooldown_minutes": 60
                },
                {
                    "id": "high_error_rate",
                    "name": "Высокий процент ошибок",
                    "condition": "error_rate > 5",
                    "severity": "warning",
                    "message": "Высокий процент ошибок: {error_rate}%",
                    "channels": ["telegram", "email"],
                    "enabled": True,
                    "cooldown_minutes": 15
                },
                {
                    "id": "server_down",
                    "name": "Сервер недоступен",
                    "condition": "server_status == 'offline'",
                    "severity": "critical",
                    "message": "Сервер {server_id} недоступен",
                    "channels": ["telegram", "email", "webhook"],
                    "enabled": True,
                    "cooldown_minutes": 1
                },
                {
                    "id": "unusual_traffic_spike",
                    "name": "Необычный всплеск трафика",
                    "condition": "traffic_increase > 200",
                    "severity": "warning",
                    "message": "Обнаружен необычный всплеск трафика: {traffic_increase}%",
                    "channels": ["telegram"],
                    "enabled": True,
                    "cooldown_minutes": 60
                },
                {
                    "id": "failed_login_attempts",
                    "name": "Множественные неудачные попытки входа",
                    "condition": "failed_logins > 10",
                    "severity": "warning",
                    "message": "Обнаружено {failed_logins} неудачных попыток входа за последний час",
                    "channels": ["telegram", "email"],
                    "enabled": True,
                    "cooldown_minutes": 30
                },
                {
                    "id": "security_incident",
                    "name": "Инцидент безопасности",
                    "condition": "security_threat_level == 'high'",
                    "severity": "critical",
                    "message": "Обнаружен инцидент безопасности: {threat_description}",
                    "channels": ["telegram", "email", "webhook"],
                    "enabled": True,
                    "cooldown_minutes": 5
                },
                {
                    "id": "low_disk_space",
                    "name": "Мало места на диске",
                    "condition": "disk_free_gb < 5",
                    "severity": "warning",
                    "message": "Мало места на диске сервера {server_id}: {disk_free_gb} GB свободно",
                    "channels": ["telegram", "email"],
                    "enabled": True,
                    "cooldown_minutes": 120
                }
            ]
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка загрузки правил алертов: {e}")
            return []
    
    async def check_all_alerts(self):
        """Проверка всех алертов"""
        try:
            if not settings.ALERTS_ENABLED:
                return
            
            # Получаем текущие метрики
            current_metrics = await self.get_current_metrics()
            
            # Проверяем каждое правило
            for rule in self.alert_rules:
                if not rule.get("enabled", True):
                    continue
                
                await self.check_alert_rule(rule, current_metrics)
                
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка проверки алертов: {e}")
    
    async def check_alert_rule(self, rule: Dict[str, Any], metrics: Dict[str, Any]):
        """Проверка конкретного правила алерта"""
        try:
            rule_id = rule["id"]
            
            # Проверяем cooldown
            if await self.is_alert_in_cooldown(rule_id):
                return
            
            # Проверяем условие
            if not await self.evaluate_condition(rule["condition"], metrics):
                return
            
            # Создаем алерт
            alert = await self.create_alert(rule, metrics)
            
            # Проверяем соответствие требованиям приватности
            if not await self.privacy_checker.validate_metrics(alert):
                logger.warning(f"[Alert Manager] Алерт {rule_id} не прошел проверку приватности")
                return
            
            # Сохраняем алерт
            await self.store_alert(alert)
            
            # Отправляем уведомления
            await self.send_notifications(alert)
            
            # Обновляем cooldown
            await self.update_cooldown(rule_id)
            
            logger.info(f"[Alert Manager] Создан алерт: {rule['name']}")
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка проверки правила {rule.get('id', 'unknown')}: {e}")
    
    async def evaluate_condition(self, condition: str, metrics: Dict[str, Any]) -> bool:
        """Оценка условия алерта"""
        try:
            # Простая система оценки условий
            # В реальной реализации здесь должна быть более сложная логика
            
            if "cpu_usage >" in condition:
                threshold = float(condition.split("cpu_usage >")[1].strip())
                cpu_usage = self.get_metric_value(metrics, "cpu_usage_percent", 0)
                return cpu_usage > threshold
            
            elif "memory_usage >" in condition:
                threshold = float(condition.split("memory_usage >")[1].strip())
                memory_usage = self.get_metric_value(metrics, "memory_usage_percent", 0)
                return memory_usage > threshold
            
            elif "disk_usage >" in condition:
                threshold = float(condition.split("disk_usage >")[1].strip())
                disk_usage = self.get_metric_value(metrics, "disk_usage_percent", 0)
                return disk_usage > threshold
            
            elif "error_rate >" in condition:
                threshold = float(condition.split("error_rate >")[1].strip())
                error_rate = self.get_metric_value(metrics, "error_rate_percent", 0)
                return error_rate > threshold
            
            elif "server_status == 'offline'" in condition:
                server_status = self.get_metric_value(metrics, "server_status", "online")
                return server_status == "offline"
            
            elif "traffic_increase >" in condition:
                threshold = float(condition.split("traffic_increase >")[1].strip())
                traffic_increase = self.get_metric_value(metrics, "traffic_increase_percent", 0)
                return traffic_increase > threshold
            
            elif "failed_logins >" in condition:
                threshold = float(condition.split("failed_logins >")[1].strip())
                failed_logins = self.get_metric_value(metrics, "failed_login_attempts", 0)
                return failed_logins > threshold
            
            elif "security_threat_level == 'high'" in condition:
                threat_level = self.get_metric_value(metrics, "security_threat_level", "low")
                return threat_level == "high"
            
            elif "disk_free_gb <" in condition:
                threshold = float(condition.split("disk_free_gb <")[1].strip())
                disk_free = self.get_metric_value(metrics, "disk_free_gb", 100)
                return disk_free < threshold
            
            return False
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка оценки условия '{condition}': {e}")
            return False
    
    def get_metric_value(self, metrics: Dict[str, Any], key: str, default: Any = None) -> Any:
        """Получение значения метрики из вложенной структуры"""
        try:
            # Поддерживаем вложенные ключи через точку
            if "." in key:
                keys = key.split(".")
                value = metrics
                for k in keys:
                    if isinstance(value, dict) and k in value:
                        value = value[k]
                    else:
                        return default
                return value
            else:
                return metrics.get(key, default)
                
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка получения значения метрики '{key}': {e}")
            return default
    
    async def create_alert(self, rule: Dict[str, Any], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Создание алерта"""
        try:
            alert_id = str(uuid.uuid4())
            
            # Создаем безопасный словарь для форматирования сообщения
            safe_metrics = {}
            for key, value in metrics.items():
                if isinstance(value, (str, int, float)):
                    safe_metrics[key] = value
                elif isinstance(value, dict):
                    # Рекурсивно обрабатываем вложенные словари
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (str, int, float)):
                            safe_metrics[f"{key}_{sub_key}"] = sub_value
            
            # Форматируем сообщение с безопасными значениями
            try:
                message = rule["message"].format(**safe_metrics)
            except KeyError as e:
                # Если не хватает ключей, используем базовое сообщение
                message = f"{rule['name']}: {rule['message']}"
            
            alert = {
                "id": alert_id,
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "severity": rule["severity"],
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": metrics,
                "status": "active",
                "escalation_level": 1,
                "channels": rule.get("channels", []),
                "acknowledged": False,
                "acknowledged_by": None,
                "acknowledged_at": None,
                "resolved": False,
                "resolved_at": None,
                "resolved_by": None
            }
            
            return alert
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка создания алерта: {e}")
            return {}
    
    async def store_alert(self, alert: Dict[str, Any]):
        """Сохранение алерта"""
        try:
            alert_id = alert["id"]
            
            # Добавляем в активные алерты
            self.active_alerts[alert_id] = alert
            
            # Добавляем в историю
            self.alert_history.append(alert)
            
            # Здесь должна быть логика сохранения в базу данных
            logger.debug(f"[Alert Manager] Алерт {alert_id} сохранен")
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка сохранения алерта: {e}")
    
    async def send_notifications(self, alert: Dict[str, Any]):
        """Отправка уведомлений"""
        try:
            channels = alert.get("channels", [])
            
            for channel in channels:
                try:
                    if channel == "telegram":
                        await self.notification_channels.send_telegram_alert(alert)
                    elif channel == "email":
                        await self.notification_channels.send_email_alert(alert)
                    elif channel == "webhook":
                        await self.notification_channels.send_webhook_alert(alert)
                        
                except Exception as e:
                    logger.error(f"[Alert Manager] Ошибка отправки уведомления через {channel}: {e}")
                    
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка отправки уведомлений: {e}")
    
    async def get_current_metrics(self) -> Dict[str, Any]:
        """Получение текущих метрик"""
        try:
            # Здесь должна быть логика получения метрик из системы мониторинга
            # Для примера возвращаем тестовые данные
            import random
            
            return {
                "cpu_usage_percent": round(random.uniform(20, 90), 2),
                "memory_usage_percent": round(random.uniform(30, 85), 2),
                "disk_usage_percent": round(random.uniform(20, 60), 2),
                "error_rate_percent": round(random.uniform(0, 5), 2),
                "server_status": random.choice(["online", "offline", "warning"]),
                "traffic_increase_percent": round(random.uniform(0, 300), 2),
                "failed_login_attempts": random.randint(0, 15),
                "security_threat_level": random.choice(["low", "medium", "high"]),
                "disk_free_gb": round(random.uniform(5, 100), 2),
                "server_id": "server_1"
            }
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка получения текущих метрик: {e}")
            return {}
    
    async def is_alert_in_cooldown(self, rule_id: str) -> bool:
        """Проверка cooldown для правила"""
        try:
            if rule_id not in self.metrics_cache:
                return False
            
            rule = next((r for r in self.alert_rules if r["id"] == rule_id), None)
            if not rule:
                return False
            
            cooldown_minutes = rule.get("cooldown_minutes", 30)
            last_alert = self.metrics_cache[rule_id].get("last_alert")
            
            if not last_alert:
                return False
            
            time_since_last = (datetime.utcnow() - last_alert).total_seconds() / 60
            return time_since_last < cooldown_minutes
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка проверки cooldown: {e}")
            return False
    
    async def update_cooldown(self, rule_id: str):
        """Обновление cooldown для правила"""
        try:
            if rule_id not in self.metrics_cache:
                self.metrics_cache[rule_id] = {}
            
            self.metrics_cache[rule_id]["last_alert"] = datetime.utcnow()
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка обновления cooldown: {e}")
    
    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Получение активных алертов"""
        try:
            return list(self.active_alerts.values())
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка получения активных алертов: {e}")
            return []
    
    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Подтверждение алерта"""
        try:
            if alert_id not in self.active_alerts:
                return False
            
            alert = self.active_alerts[alert_id]
            alert["acknowledged"] = True
            alert["acknowledged_by"] = acknowledged_by
            alert["acknowledged_at"] = datetime.utcnow().isoformat()
            
            logger.info(f"[Alert Manager] Алерт {alert_id} подтвержден пользователем {acknowledged_by}")
            return True
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка подтверждения алерта {alert_id}: {e}")
            return False
    
    async def resolve_alert(self, alert_id: str, resolved_by: str) -> bool:
        """Разрешение алерта"""
        try:
            if alert_id not in self.active_alerts:
                return False
            
            alert = self.active_alerts[alert_id]
            alert["resolved"] = True
            alert["resolved_at"] = datetime.utcnow().isoformat()
            alert["resolved_by"] = resolved_by
            alert["status"] = "resolved"
            
            # Удаляем из активных алертов
            del self.active_alerts[alert_id]
            
            logger.info(f"[Alert Manager] Алерт {alert_id} разрешен пользователем {resolved_by}")
            return True
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка разрешения алерта {alert_id}: {e}")
            return False
    
    async def get_alert_statistics(self) -> Dict[str, Any]:
        """Получение статистики алертов"""
        try:
            active_count = len(self.active_alerts)
            total_history = len(self.alert_history)
            
            # Статистика по серьезности
            severity_stats = defaultdict(int)
            for alert in self.alert_history:
                severity_stats[alert.get("severity", "unknown")] += 1
            
            # Статистика за последние 24 часа
            last_24h = datetime.utcnow() - timedelta(hours=24)
            recent_alerts = [
                alert for alert in self.alert_history
                if datetime.fromisoformat(alert["timestamp"]) > last_24h
            ]
            
            return {
                "active_alerts": active_count,
                "total_alerts": total_history,
                "alerts_24h": len(recent_alerts),
                "severity_distribution": dict(severity_stats),
                "resolution_rate": round(
                    len([a for a in self.alert_history if a.get("resolved", False)]) / max(total_history, 1) * 100, 2
                ),
                "avg_resolution_time_minutes": await self.calculate_avg_resolution_time()
            }
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка получения статистики алертов: {e}")
            return {}
    
    async def calculate_avg_resolution_time(self) -> float:
        """Расчет среднего времени разрешения алертов"""
        try:
            resolved_alerts = [
                alert for alert in self.alert_history
                if alert.get("resolved", False) and alert.get("resolved_at")
            ]
            
            if not resolved_alerts:
                return 0.0
            
            total_time = 0
            for alert in resolved_alerts:
                created_at = datetime.fromisoformat(alert["timestamp"])
                resolved_at = datetime.fromisoformat(alert["resolved_at"])
                resolution_time = (resolved_at - created_at).total_seconds() / 60  # минуты
                total_time += resolution_time
            
            return round(total_time / len(resolved_alerts), 2)
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка расчета времени разрешения: {e}")
            return 0.0
    
    async def update_alert_rule(self, rule_id: str, updates: Dict[str, Any]) -> bool:
        """Обновление правила алерта"""
        try:
            for i, rule in enumerate(self.alert_rules):
                if rule["id"] == rule_id:
                    self.alert_rules[i].update(updates)
                    logger.info(f"[Alert Manager] Правило {rule_id} обновлено")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка обновления правила {rule_id}: {e}")
            return False
    
    async def delete_alert_rule(self, rule_id: str) -> bool:
        """Удаление правила алерта"""
        try:
            self.alert_rules = [rule for rule in self.alert_rules if rule["id"] != rule_id]
            logger.info(f"[Alert Manager] Правило {rule_id} удалено")
            return True
            
        except Exception as e:
            logger.error(f"[Alert Manager] Ошибка удаления правила {rule_id}: {e}")
            return False
