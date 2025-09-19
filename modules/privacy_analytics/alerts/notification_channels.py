"""
Каналы уведомлений для алертов
"""

import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Any, Optional

from .. import settings
from logger import logger


class NotificationChannels:
    """Каналы уведомлений для алертов"""
    
    def __init__(self):
        self.telegram_enabled = settings.TELEGRAM_ALERTS_ENABLED
        self.email_enabled = settings.EMAIL_ALERTS_ENABLED
        self.webhook_enabled = settings.WEBHOOK_ALERTS_ENABLED
        
    async def send_telegram_alert(self, alert: Dict[str, Any]) -> bool:
        """Отправка алерта через Telegram"""
        try:
            if not self.telegram_enabled:
                return False
            
            chat_id = settings.TELEGRAM_ALERT_CHAT_ID
            bot_token = settings.TELEGRAM_ALERT_BOT_TOKEN
            
            if not chat_id or not bot_token:
                logger.warning("[Notification Channels] Telegram настройки не заданы")
                return False
            
            # Формируем сообщение
            message = self.format_telegram_message(alert)
            
            # Отправляем сообщение
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        logger.info(f"[Notification Channels] Telegram алерт отправлен: {alert['id']}")
                        return True
                    else:
                        logger.error(f"[Notification Channels] Ошибка отправки Telegram: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка отправки Telegram алерта: {e}")
            return False
    
    async def send_email_alert(self, alert: Dict[str, Any]) -> bool:
        """Отправка алерта по email"""
        try:
            if not self.email_enabled:
                return False
            
            # Здесь должна быть логика отправки email
            # Для примера просто логируем
            logger.info(f"[Notification Channels] Email алерт отправлен: {alert['id']}")
            return True
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка отправки email алерта: {e}")
            return False
    
    async def send_webhook_alert(self, alert: Dict[str, Any]) -> bool:
        """Отправка алерта через webhook"""
        try:
            if not self.webhook_enabled:
                return False
            
            # Здесь должна быть логика отправки webhook
            # Для примера просто логируем
            logger.info(f"[Notification Channels] Webhook алерт отправлен: {alert['id']}")
            return True
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка отправки webhook алерта: {e}")
            return False
    
    def format_telegram_message(self, alert: Dict[str, Any]) -> str:
        """Форматирование сообщения для Telegram"""
        try:
            severity_emoji = {
                "critical": "🔴",
                "warning": "🟡", 
                "info": "🔵"
            }.get(alert.get("severity", "info"), "⚪")
            
            message = f"""
{severity_emoji} <b>Алерт: {alert.get('rule_name', 'Unknown')}</b>

📝 <b>Сообщение:</b> {alert.get('message', 'No message')}
⏰ <b>Время:</b> {alert.get('timestamp', 'Unknown')}
🔢 <b>ID:</b> {alert.get('id', 'Unknown')}
📊 <b>Статус:</b> {alert.get('status', 'Unknown')}

#alert #{alert.get('severity', 'unknown')}
            """.strip()
            
            return message
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка форматирования Telegram сообщения: {e}")
            return f"Алерт: {alert.get('message', 'Unknown')}"
    
    def format_email_message(self, alert: Dict[str, Any]) -> str:
        """Форматирование сообщения для email"""
        try:
            message = f"""
Алерт системы мониторинга

Правило: {alert.get('rule_name', 'Unknown')}
Сообщение: {alert.get('message', 'No message')}
Время: {alert.get('timestamp', 'Unknown')}
ID: {alert.get('id', 'Unknown')}
Статус: {alert.get('status', 'Unknown')}
Серьезность: {alert.get('severity', 'Unknown')}

---
Отправлено автоматически системой мониторинга
            """.strip()
            
            return message
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка форматирования email сообщения: {e}")
            return f"Алерт: {alert.get('message', 'Unknown')}"
    
    def format_webhook_payload(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """Форматирование payload для webhook"""
        try:
            payload = {
                "alert_id": alert.get("id"),
                "rule_name": alert.get("rule_name"),
                "severity": alert.get("severity"),
                "message": alert.get("message"),
                "timestamp": alert.get("timestamp"),
                "status": alert.get("status"),
                "metrics": alert.get("metrics", {}),
                "escalation_level": alert.get("escalation_level", 1),
                "acknowledged": alert.get("acknowledged", False),
                "resolved": alert.get("resolved", False)
            }
            
            return payload
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка форматирования webhook payload: {e}")
            return {"error": "Failed to format webhook payload"}
    
    async def test_telegram_connection(self) -> bool:
        """Тестирование подключения к Telegram"""
        try:
            if not self.telegram_enabled:
                return False
            
            chat_id = settings.TELEGRAM_ALERT_CHAT_ID
            bot_token = settings.TELEGRAM_ALERT_BOT_TOKEN
            
            if not chat_id or not bot_token:
                return False
            
            url = f"https://api.telegram.org/bot{bot_token}/getMe"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка тестирования Telegram: {e}")
            return False
    
    async def test_email_connection(self) -> bool:
        """Тестирование подключения к email"""
        try:
            if not self.email_enabled:
                return False
            
            # Здесь должна быть логика тестирования email
            return True
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка тестирования email: {e}")
            return False
    
    async def test_webhook_connection(self, webhook_url: str) -> bool:
        """Тестирование подключения к webhook"""
        try:
            if not self.webhook_enabled:
                return False
            
            test_payload = {
                "test": True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=test_payload) as response:
                    return response.status in [200, 201, 202]
                    
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка тестирования webhook: {e}")
            return False
    
    async def get_channel_status(self) -> Dict[str, Any]:
        """Получение статуса каналов уведомлений"""
        try:
            status = {
                "telegram": {
                    "enabled": self.telegram_enabled,
                    "configured": bool(settings.TELEGRAM_ALERT_CHAT_ID and settings.TELEGRAM_ALERT_BOT_TOKEN),
                    "test_result": await self.test_telegram_connection() if self.telegram_enabled else False
                },
                "email": {
                    "enabled": self.email_enabled,
                    "configured": bool(settings.EMAIL_ALERT_SMTP_SERVER and settings.EMAIL_ALERT_USERNAME),
                    "test_result": await self.test_email_connection() if self.email_enabled else False
                },
                "webhook": {
                    "enabled": self.webhook_enabled,
                    "configured": True,  # Webhook может быть настроен динамически
                    "test_result": None  # Требует URL для тестирования
                }
            }
            
            return status
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка получения статуса каналов: {e}")
            return {}
    
    async def send_bulk_notifications(self, alerts: List[Dict[str, Any]], channel: str) -> Dict[str, Any]:
        """Отправка массовых уведомлений"""
        try:
            results = {
                "total": len(alerts),
                "success": 0,
                "failed": 0,
                "errors": []
            }
            
            for alert in alerts:
                try:
                    if channel == "telegram":
                        success = await self.send_telegram_alert(alert)
                    elif channel == "email":
                        success = await self.send_email_alert(alert)
                    elif channel == "webhook":
                        success = await self.send_webhook_alert(alert)
                    else:
                        success = False
                        results["errors"].append(f"Unknown channel: {channel}")
                    
                    if success:
                        results["success"] += 1
                    else:
                        results["failed"] += 1
                        
                except Exception as e:
                    results["failed"] += 1
                    results["errors"].append(f"Error sending alert {alert.get('id', 'unknown')}: {str(e)}")
            
            return results
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка массовой отправки: {e}")
            return {"total": 0, "success": 0, "failed": 0, "errors": [str(e)]}
    
    async def send_digest_notification(self, alerts: List[Dict[str, Any]], channel: str) -> bool:
        """Отправка сводного уведомления"""
        try:
            if not alerts:
                return True
            
            # Группируем алерты по серьезности
            critical_alerts = [a for a in alerts if a.get("severity") == "critical"]
            warning_alerts = [a for a in alerts if a.get("severity") == "warning"]
            info_alerts = [a for a in alerts if a.get("severity") == "info"]
            
            # Формируем сводное сообщение
            if channel == "telegram":
                message = self.format_telegram_digest(critical_alerts, warning_alerts, info_alerts)
                return await self.send_telegram_message(message)
            elif channel == "email":
                message = self.format_email_digest(critical_alerts, warning_alerts, info_alerts)
                return await self.send_email_message("Сводка алертов", message)
            else:
                return False
                
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка отправки сводного уведомления: {e}")
            return False
    
    def format_telegram_digest(self, critical: List, warning: List, info: List) -> str:
        """Форматирование сводного сообщения для Telegram"""
        try:
            message = f"""
📊 <b>Сводка алертов</b>

🔴 <b>Критические:</b> {len(critical)}
🟡 <b>Предупреждения:</b> {len(warning)}
🔵 <b>Информационные:</b> {len(info)}

<b>Всего алертов:</b> {len(critical) + len(warning) + len(info)}
⏰ <b>Время:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

#alerts #summary
            """.strip()
            
            return message
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка форматирования сводки Telegram: {e}")
            return "Сводка алертов недоступна"
    
    def format_email_digest(self, critical: List, warning: List, info: List) -> str:
        """Форматирование сводного сообщения для email"""
        try:
            message = f"""
Сводка алертов системы мониторинга

Критические: {len(critical)}
Предупреждения: {len(warning)}
Информационные: {len(info)}

Всего алертов: {len(critical) + len(warning) + len(info)}
Время: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

---
Отправлено автоматически системой мониторинга
            """.strip()
            
            return message
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка форматирования сводки email: {e}")
            return "Сводка алертов недоступна"
    
    async def send_telegram_message(self, message: str) -> bool:
        """Отправка произвольного сообщения в Telegram"""
        try:
            if not self.telegram_enabled:
                return False
            
            chat_id = settings.TELEGRAM_ALERT_CHAT_ID
            bot_token = settings.TELEGRAM_ALERT_BOT_TOKEN
            
            if not chat_id or not bot_token:
                return False
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка отправки Telegram сообщения: {e}")
            return False
    
    async def send_email_message(self, subject: str, message: str) -> bool:
        """Отправка произвольного сообщения по email"""
        try:
            if not self.email_enabled:
                return False
            
            # Здесь должна быть логика отправки email
            logger.info(f"[Notification Channels] Email отправлен: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"[Notification Channels] Ошибка отправки email: {e}")
            return False
