"""
Правила эскалации алертов
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

from .. import settings
from logger import logger


class EscalationLevel(Enum):
    """Уровни эскалации"""
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL_4 = 4
    LEVEL_5 = 5


class EscalationRules:
    """Правила эскалации алертов"""
    
    def __init__(self):
        self.escalation_configs = self.load_escalation_configs()
        self.escalation_timers = {}
        
    def load_escalation_configs(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка конфигураций эскалации"""
        try:
            return {
                "critical": {
                    "levels": [
                        {
                            "level": 1,
                            "delay_minutes": 5,
                            "channels": ["telegram", "email"],
                            "recipients": ["admin1", "admin2"],
                            "message_template": "КРИТИЧЕСКИЙ АЛЕРТ: {message}"
                        },
                        {
                            "level": 2,
                            "delay_minutes": 15,
                            "channels": ["telegram", "email", "webhook"],
                            "recipients": ["admin1", "admin2", "manager1"],
                            "message_template": "ЭСКАЛАЦИЯ КРИТИЧЕСКОГО АЛЕРТА: {message}"
                        },
                        {
                            "level": 3,
                            "delay_minutes": 30,
                            "channels": ["telegram", "email", "webhook", "sms"],
                            "recipients": ["admin1", "admin2", "manager1", "director"],
                            "message_template": "ВЫСОКАЯ ЭСКАЛАЦИЯ: {message}"
                        }
                    ],
                    "max_level": 3,
                    "auto_resolve_after_hours": 24
                },
                "warning": {
                    "levels": [
                        {
                            "level": 1,
                            "delay_minutes": 30,
                            "channels": ["telegram"],
                            "recipients": ["admin1"],
                            "message_template": "ПРЕДУПРЕЖДЕНИЕ: {message}"
                        },
                        {
                            "level": 2,
                            "delay_minutes": 120,
                            "channels": ["telegram", "email"],
                            "recipients": ["admin1", "admin2"],
                            "message_template": "ЭСКАЛАЦИЯ ПРЕДУПРЕЖДЕНИЯ: {message}"
                        }
                    ],
                    "max_level": 2,
                    "auto_resolve_after_hours": 12
                },
                "info": {
                    "levels": [
                        {
                            "level": 1,
                            "delay_minutes": 60,
                            "channels": ["telegram"],
                            "recipients": ["admin1"],
                            "message_template": "ИНФОРМАЦИЯ: {message}"
                        }
                    ],
                    "max_level": 1,
                    "auto_resolve_after_hours": 6
                }
            }
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка загрузки конфигураций эскалации: {e}")
            return {}
    
    async def check_escalation(self, alert: Dict[str, Any]) -> bool:
        """Проверка необходимости эскалации"""
        try:
            alert_id = alert["id"]
            severity = alert.get("severity", "info")
            current_level = alert.get("escalation_level", 1)
            
            # Получаем конфигурацию для данного уровня серьезности
            config = self.escalation_configs.get(severity)
            if not config:
                return False
            
            # Проверяем, не достигли ли максимального уровня
            if current_level >= config["max_level"]:
                return False
            
            # Проверяем, не находится ли алерт в процессе эскалации
            if alert_id in self.escalation_timers:
                return False
            
            # Получаем следующий уровень эскалации
            next_level_config = next(
                (level for level in config["levels"] if level["level"] == current_level + 1),
                None
            )
            
            if not next_level_config:
                return False
            
            # Запускаем таймер эскалации
            await self.start_escalation_timer(alert, next_level_config)
            
            return True
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка проверки эскалации: {e}")
            return False
    
    async def start_escalation_timer(self, alert: Dict[str, Any], level_config: Dict[str, Any]):
        """Запуск таймера эскалации"""
        try:
            alert_id = alert["id"]
            delay_minutes = level_config["delay_minutes"]
            
            # Создаем задачу эскалации
            escalation_task = asyncio.create_task(
                self.execute_escalation(alert, level_config, delay_minutes)
            )
            
            # Сохраняем таймер
            self.escalation_timers[alert_id] = {
                "task": escalation_task,
                "level": level_config["level"],
                "scheduled_time": datetime.utcnow() + timedelta(minutes=delay_minutes)
            }
            
            logger.info(f"[Escalation Rules] Таймер эскалации запущен для алерта {alert_id}, уровень {level_config['level']}")
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка запуска таймера эскалации: {e}")
    
    async def execute_escalation(self, alert: Dict[str, Any], level_config: Dict[str, Any], delay_minutes: int):
        """Выполнение эскалации"""
        try:
            # Ждем указанное время
            await asyncio.sleep(delay_minutes * 60)
            
            alert_id = alert["id"]
            
            # Проверяем, не был ли алерт разрешен за это время
            if alert_id not in self.escalation_timers:
                return
            
            # Обновляем уровень эскалации
            alert["escalation_level"] = level_config["level"]
            
            # Формируем сообщение эскалации
            escalated_message = level_config["message_template"].format(
                message=alert.get("message", "Unknown")
            )
            
            # Создаем новый алерт для эскалации
            escalated_alert = alert.copy()
            escalated_alert["message"] = escalated_message
            escalated_alert["escalation_level"] = level_config["level"]
            escalated_alert["timestamp"] = datetime.utcnow().isoformat()
            escalated_alert["channels"] = level_config["channels"]
            escalated_alert["recipients"] = level_config["recipients"]
            
            # Отправляем уведомления эскалации
            await self.send_escalation_notifications(escalated_alert, level_config)
            
            # Удаляем таймер
            if alert_id in self.escalation_timers:
                del self.escalation_timers[alert_id]
            
            logger.info(f"[Escalation Rules] Эскалация выполнена для алерта {alert_id}, уровень {level_config['level']}")
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка выполнения эскалации: {e}")
    
    async def send_escalation_notifications(self, alert: Dict[str, Any], level_config: Dict[str, Any]):
        """Отправка уведомлений эскалации"""
        try:
            channels = level_config.get("channels", [])
            recipients = level_config.get("recipients", [])
            
            # Здесь должна быть логика отправки уведомлений через различные каналы
            # Для примера просто логируем
            logger.info(f"[Escalation Rules] Отправка уведомлений эскалации: {alert['id']}")
            logger.info(f"[Escalation Rules] Каналы: {channels}, Получатели: {recipients}")
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка отправки уведомлений эскалации: {e}")
    
    async def cancel_escalation(self, alert_id: str) -> bool:
        """Отмена эскалации"""
        try:
            if alert_id not in self.escalation_timers:
                return False
            
            # Отменяем задачу эскалации
            escalation_data = self.escalation_timers[alert_id]
            escalation_data["task"].cancel()
            
            # Удаляем таймер
            del self.escalation_timers[alert_id]
            
            logger.info(f"[Escalation Rules] Эскалация отменена для алерта {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка отмены эскалации: {e}")
            return False
    
    async def get_escalation_status(self, alert_id: str) -> Dict[str, Any]:
        """Получение статуса эскалации"""
        try:
            if alert_id not in self.escalation_timers:
                return {"escalating": False}
            
            escalation_data = self.escalation_timers[alert_id]
            
            return {
                "escalating": True,
                "current_level": escalation_data["level"],
                "scheduled_time": escalation_data["scheduled_time"].isoformat(),
                "time_remaining_minutes": max(0, int(
                    (escalation_data["scheduled_time"] - datetime.utcnow()).total_seconds() / 60
                ))
            }
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка получения статуса эскалации: {e}")
            return {"escalating": False}
    
    async def get_all_escalations(self) -> List[Dict[str, Any]]:
        """Получение всех активных эскалаций"""
        try:
            escalations = []
            
            for alert_id, escalation_data in self.escalation_timers.items():
                escalations.append({
                    "alert_id": alert_id,
                    "level": escalation_data["level"],
                    "scheduled_time": escalation_data["scheduled_time"].isoformat(),
                    "time_remaining_minutes": max(0, int(
                        (escalation_data["scheduled_time"] - datetime.utcnow()).total_seconds() / 60
                    ))
                })
            
            return escalations
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка получения всех эскалаций: {e}")
            return []
    
    async def update_escalation_config(self, severity: str, config: Dict[str, Any]) -> bool:
        """Обновление конфигурации эскалации"""
        try:
            self.escalation_configs[severity] = config
            logger.info(f"[Escalation Rules] Конфигурация эскалации обновлена для {severity}")
            return True
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка обновления конфигурации: {e}")
            return False
    
    async def get_escalation_config(self, severity: str) -> Dict[str, Any]:
        """Получение конфигурации эскалации"""
        try:
            return self.escalation_configs.get(severity, {})
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка получения конфигурации: {e}")
            return {}
    
    async def cleanup_expired_escalations(self):
        """Очистка истекших эскалаций"""
        try:
            current_time = datetime.utcnow()
            expired_alerts = []
            
            for alert_id, escalation_data in self.escalation_timers.items():
                # Проверяем, не истекла ли эскалация
                if current_time > escalation_data["scheduled_time"] + timedelta(hours=1):
                    expired_alerts.append(alert_id)
            
            # Удаляем истекшие эскалации
            for alert_id in expired_alerts:
                await self.cancel_escalation(alert_id)
            
            if expired_alerts:
                logger.info(f"[Escalation Rules] Очищено {len(expired_alerts)} истекших эскалаций")
                
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка очистки истекших эскалаций: {e}")
    
    async def get_escalation_statistics(self) -> Dict[str, Any]:
        """Получение статистики эскалаций"""
        try:
            total_escalations = len(self.escalation_timers)
            
            # Группируем по уровням
            level_distribution = {}
            for escalation_data in self.escalation_timers.values():
                level = escalation_data["level"]
                level_distribution[level] = level_distribution.get(level, 0) + 1
            
            # Группируем по времени до эскалации
            time_distribution = {
                "immediate": 0,
                "within_1_hour": 0,
                "within_24_hours": 0,
                "more_than_24_hours": 0
            }
            
            current_time = datetime.utcnow()
            for escalation_data in self.escalation_timers.values():
                time_remaining = (escalation_data["scheduled_time"] - current_time).total_seconds() / 3600
                
                if time_remaining <= 0:
                    time_distribution["immediate"] += 1
                elif time_remaining <= 1:
                    time_distribution["within_1_hour"] += 1
                elif time_remaining <= 24:
                    time_distribution["within_24_hours"] += 1
                else:
                    time_distribution["more_than_24_hours"] += 1
            
            return {
                "total_active_escalations": total_escalations,
                "level_distribution": level_distribution,
                "time_distribution": time_distribution,
                "escalation_configs": {
                    severity: {
                        "max_level": config["max_level"],
                        "levels_count": len(config["levels"])
                    }
                    for severity, config in self.escalation_configs.items()
                }
            }
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка получения статистики эскалаций: {e}")
            return {}
    
    async def force_escalation(self, alert: Dict[str, Any], target_level: int) -> bool:
        """Принудительная эскалация"""
        try:
            alert_id = alert["id"]
            severity = alert.get("severity", "info")
            
            # Получаем конфигурацию для целевого уровня
            config = self.escalation_configs.get(severity)
            if not config:
                return False
            
            level_config = next(
                (level for level in config["levels"] if level["level"] == target_level),
                None
            )
            
            if not level_config:
                return False
            
            # Отменяем текущую эскалацию, если есть
            await self.cancel_escalation(alert_id)
            
            # Выполняем принудительную эскалацию
            await self.execute_escalation(alert, level_config, 0)
            
            logger.info(f"[Escalation Rules] Принудительная эскалация выполнена для алерта {alert_id}, уровень {target_level}")
            return True
            
        except Exception as e:
            logger.error(f"[Escalation Rules] Ошибка принудительной эскалации: {e}")
            return False
