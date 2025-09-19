"""
Мониторинг безопасности
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque

from .. import settings
from ..privacy import PrivacyComplianceChecker
from logger import logger


class SecurityMonitor:
    """Мониторинг событий безопасности"""
    
    def __init__(self):
        self.privacy_checker = PrivacyComplianceChecker()
        self.security_events = deque(maxlen=10000)
        self.failed_logins = defaultdict(list)
        self.suspicious_ips = defaultdict(int)
        self.privilege_attempts = deque(maxlen=1000)
        self.unauthorized_access = deque(maxlen=1000)
        
    async def monitor_security_events(self):
        """Мониторинг событий безопасности"""
        try:
            # Детекция угроз
            threat_events = await self.detect_threats()
            
            # Контроль доступа
            access_events = await self.monitor_access_control()
            
            # Защита данных
            data_protection_events = await self.monitor_data_protection()
            
            # Объединяем все события
            security_events = {
                "timestamp": datetime.utcnow().isoformat(),
                "threat_detection": threat_events,
                "access_control": access_events,
                "data_protection": data_protection_events
            }
            
            # Проверяем соответствие требованиям приватности
            if not self.privacy_checker.validate_metrics(security_events):
                logger.warning("[Security Monitor] События безопасности не прошли проверку приватности")
                return
            
            # Сохраняем события
            await self.store_security_events(security_events)
            
            # Проверяем алерты безопасности
            await self.check_security_alerts(security_events)
            
            logger.debug("[Security Monitor] События безопасности обработаны успешно")
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка мониторинга безопасности: {e}")
    
    async def detect_threats(self) -> Dict[str, Any]:
        """Детекция угроз безопасности"""
        try:
            # Анализируем неудачные попытки входа
            failed_logins = await self.analyze_failed_logins()
            
            # Анализируем подозрительную активность IP
            suspicious_activity = await self.analyze_suspicious_ips()
            
            # Анализируем попытки брутфорса
            brute_force_attempts = await self.detect_brute_force()
            
            # Анализируем необычные паттерны трафика
            unusual_patterns = await self.detect_unusual_patterns()
            
            return {
                "failed_login_attempts": failed_logins,
                "suspicious_ip_activity": suspicious_activity,
                "brute_force_attempts": brute_force_attempts,
                "unusual_traffic_patterns": unusual_patterns,
                "threat_level": await self.calculate_threat_level()
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка детекции угроз: {e}")
            return {}
    
    async def monitor_access_control(self) -> Dict[str, Any]:
        """Мониторинг контроля доступа"""
        try:
            # Административные действия
            admin_actions = await self.get_admin_actions_count()
            
            # Попытки эскалации привилегий
            privilege_escalation = await self.get_privilege_escalation_attempts()
            
            # Несанкционированные попытки доступа
            unauthorized_access = await self.get_unauthorized_access_attempts()
            
            # Анализ сессий
            session_analysis = await self.analyze_sessions()
            
            return {
                "admin_actions_count": admin_actions,
                "privilege_escalation_attempts": privilege_escalation,
                "unauthorized_access_attempts": unauthorized_access,
                "session_analysis": session_analysis
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка мониторинга доступа: {e}")
            return {}
    
    async def monitor_data_protection(self) -> Dict[str, Any]:
        """Мониторинг защиты данных"""
        try:
            # Попытки нарушения приватности
            privacy_violations = await self.get_privacy_violation_attempts()
            
            # Индикаторы утечки данных
            data_breach_indicators = await self.get_data_breach_indicators()
            
            # Нарушения соответствия требованиям
            compliance_violations = await self.get_compliance_violations()
            
            # Аудит доступа к данным
            data_access_audit = await self.audit_data_access()
            
            return {
                "privacy_violation_attempts": privacy_violations,
                "data_breach_indicators": data_breach_indicators,
                "compliance_violations": compliance_violations,
                "data_access_audit": data_access_audit
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка мониторинга защиты данных: {e}")
            return {}
    
    async def analyze_failed_logins(self) -> Dict[str, Any]:
        """Анализ неудачных попыток входа"""
        try:
            # Очищаем старые записи (старше 1 часа)
            cutoff_time = time.time() - 3600
            for ip in list(self.failed_logins.keys()):
                self.failed_logins[ip] = [
                    timestamp for timestamp in self.failed_logins[ip] 
                    if timestamp > cutoff_time
                ]
                if not self.failed_logins[ip]:
                    del self.failed_logins[ip]
            
            # Подсчитываем статистику
            total_failed = sum(len(attempts) for attempts in self.failed_logins.values())
            unique_ips = len(self.failed_logins)
            
            # Находим наиболее активные IP
            top_ips = sorted(
                self.failed_logins.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )[:10]
            
            return {
                "total_failed_attempts": total_failed,
                "unique_ips": unique_ips,
                "top_offending_ips": [
                    {"ip": ip, "attempts": len(attempts)} 
                    for ip, attempts in top_ips
                ],
                "rate_per_hour": total_failed
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка анализа неудачных входов: {e}")
            return {}
    
    async def analyze_suspicious_ips(self) -> Dict[str, Any]:
        """Анализ подозрительной активности IP"""
        try:
            # Очищаем старые записи
            cutoff_time = time.time() - 3600
            self.suspicious_ips = {
                ip: count for ip, count in self.suspicious_ips.items()
                if count > 0
            }
            
            # Находим подозрительные IP
            suspicious_ips = [
                {"ip": ip, "suspicious_events": count}
                for ip, count in self.suspicious_ips.items()
                if count >= 5  # Порог подозрительности
            ]
            
            return {
                "suspicious_ips_count": len(suspicious_ips),
                "suspicious_ips": suspicious_ips,
                "total_suspicious_events": sum(self.suspicious_ips.values())
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка анализа подозрительных IP: {e}")
            return {}
    
    async def detect_brute_force(self) -> Dict[str, Any]:
        """Детекция попыток брутфорса"""
        try:
            brute_force_attempts = 0
            brute_force_ips = []
            
            # Анализируем IP с множественными неудачными попытками
            for ip, attempts in self.failed_logins.items():
                if len(attempts) >= 10:  # Порог для брутфорса
                    brute_force_attempts += len(attempts)
                    brute_force_ips.append({
                        "ip": ip,
                        "attempts": len(attempts),
                        "timeframe": "1 hour"
                    })
            
            return {
                "brute_force_attempts": brute_force_attempts,
                "brute_force_ips": brute_force_ips,
                "is_brute_force_active": len(brute_force_ips) > 0
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка детекции брутфорса: {e}")
            return {}
    
    async def detect_unusual_patterns(self) -> Dict[str, Any]:
        """Детекция необычных паттернов трафика"""
        try:
            # Здесь должна быть логика анализа трафика
            # Для примера возвращаем тестовые данные
            import random
            
            return {
                "unusual_traffic_spikes": random.randint(0, 3),
                "anomalous_connection_patterns": random.randint(0, 2),
                "suspicious_geographic_activity": random.randint(0, 1),
                "unusual_time_patterns": random.randint(0, 2)
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка детекции необычных паттернов: {e}")
            return {}
    
    async def calculate_threat_level(self) -> str:
        """Расчет уровня угрозы"""
        try:
            threat_score = 0
            
            # Анализируем неудачные входы
            total_failed = sum(len(attempts) for attempts in self.failed_logins.values())
            if total_failed > 50:
                threat_score += 3
            elif total_failed > 20:
                threat_score += 2
            elif total_failed > 10:
                threat_score += 1
            
            # Анализируем подозрительные IP
            suspicious_count = len([
                ip for ip, count in self.suspicious_ips.items() 
                if count >= 5
            ])
            if suspicious_count > 5:
                threat_score += 3
            elif suspicious_count > 2:
                threat_score += 2
            elif suspicious_count > 0:
                threat_score += 1
            
            # Анализируем брутфорс
            brute_force_count = len([
                ip for ip, attempts in self.failed_logins.items()
                if len(attempts) >= 10
            ])
            if brute_force_count > 0:
                threat_score += 3
            
            # Определяем уровень угрозы
            if threat_score >= 6:
                return "critical"
            elif threat_score >= 4:
                return "high"
            elif threat_score >= 2:
                return "medium"
            else:
                return "low"
                
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка расчета уровня угрозы: {e}")
            return "unknown"
    
    async def get_admin_actions_count(self) -> int:
        """Получение количества административных действий"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return random.randint(5, 25)
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка получения админских действий: {e}")
            return 0
    
    async def get_privilege_escalation_attempts(self) -> int:
        """Получение количества попыток эскалации привилегий"""
        try:
            # Очищаем старые записи
            cutoff_time = time.time() - 86400  # 24 часа
            self.privilege_attempts = deque([
                attempt for attempt in self.privilege_attempts
                if attempt > cutoff_time
            ], maxlen=1000)
            
            return len(self.privilege_attempts)
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка получения попыток эскалации: {e}")
            return 0
    
    async def get_unauthorized_access_attempts(self) -> int:
        """Получение количества попыток несанкционированного доступа"""
        try:
            # Очищаем старые записи
            cutoff_time = time.time() - 86400  # 24 часа
            self.unauthorized_access = deque([
                attempt for attempt in self.unauthorized_access
                if attempt > cutoff_time
            ], maxlen=1000)
            
            return len(self.unauthorized_access)
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка получения несанкционированного доступа: {e}")
            return 0
    
    async def analyze_sessions(self) -> Dict[str, Any]:
        """Анализ сессий пользователей"""
        try:
            # Здесь должна быть логика анализа сессий
            import random
            
            return {
                "active_sessions": random.randint(50, 200),
                "suspicious_sessions": random.randint(0, 3),
                "long_running_sessions": random.randint(5, 15),
                "sessions_from_multiple_ips": random.randint(0, 2)
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка анализа сессий: {e}")
            return {}
    
    async def get_privacy_violation_attempts(self) -> int:
        """Получение количества попыток нарушения приватности"""
        try:
            # Здесь должна быть логика проверки нарушений приватности
            import random
            return random.randint(0, 5)
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка получения нарушений приватности: {e}")
            return 0
    
    async def get_data_breach_indicators(self) -> int:
        """Получение количества индикаторов утечки данных"""
        try:
            # Здесь должна быть логика проверки утечек
            import random
            return random.randint(0, 2)
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка получения индикаторов утечки: {e}")
            return 0
    
    async def get_compliance_violations(self) -> int:
        """Получение количества нарушений соответствия требованиям"""
        try:
            # Здесь должна быть логика проверки соответствия
            import random
            return random.randint(0, 3)
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка получения нарушений соответствия: {e}")
            return 0
    
    async def audit_data_access(self) -> Dict[str, Any]:
        """Аудит доступа к данным"""
        try:
            # Здесь должна быть логика аудита доступа
            import random
            
            return {
                "data_access_events": random.randint(100, 500),
                "sensitive_data_access": random.randint(10, 50),
                "unauthorized_data_access": random.randint(0, 5),
                "data_export_events": random.randint(5, 20)
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка аудита доступа к данным: {e}")
            return {}
    
    async def store_security_events(self, events: Dict[str, Any]):
        """Сохранение событий безопасности"""
        try:
            # Добавляем в очередь событий
            self.security_events.append(events)
            
            # Здесь должна быть логика сохранения в базу данных
            logger.debug("[Security Monitor] Сохранение событий безопасности")
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка сохранения событий: {e}")
    
    async def check_security_alerts(self, events: Dict[str, Any]):
        """Проверка алертов безопасности"""
        try:
            threat_level = events.get("threat_detection", {}).get("threat_level", "low")
            
            if threat_level == "critical":
                await self.trigger_critical_alert(events)
            elif threat_level == "high":
                await self.trigger_high_alert(events)
            elif threat_level == "medium":
                await self.trigger_medium_alert(events)
                
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка проверки алертов: {e}")
    
    async def trigger_critical_alert(self, events: Dict[str, Any]):
        """Срабатывание критического алерта"""
        logger.critical("[Security Monitor] КРИТИЧЕСКИЙ АЛЕРТ БЕЗОПАСНОСТИ")
        # Здесь должна быть логика отправки критических уведомлений
    
    async def trigger_high_alert(self, events: Dict[str, Any]):
        """Срабатывание высокого алерта"""
        logger.warning("[Security Monitor] ВЫСОКИЙ АЛЕРТ БЕЗОПАСНОСТИ")
        # Здесь должна быть логика отправки высоких уведомлений
    
    async def trigger_medium_alert(self, events: Dict[str, Any]):
        """Срабатывание среднего алерта"""
        logger.info("[Security Monitor] СРЕДНИЙ АЛЕРТ БЕЗОПАСНОСТИ")
        # Здесь должна быть логика отправки средних уведомлений
    
    def record_failed_login(self, ip: str):
        """Запись неудачной попытки входа"""
        try:
            self.failed_logins[ip].append(time.time())
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка записи неудачного входа: {e}")
    
    def record_suspicious_activity(self, ip: str):
        """Запись подозрительной активности"""
        try:
            self.suspicious_ips[ip] += 1
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка записи подозрительной активности: {e}")
    
    def record_privilege_escalation(self):
        """Запись попытки эскалации привилегий"""
        try:
            self.privilege_attempts.append(time.time())
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка записи эскалации привилегий: {e}")
    
    def record_unauthorized_access(self):
        """Запись несанкционированного доступа"""
        try:
            self.unauthorized_access.append(time.time())
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка записи несанкционированного доступа: {e}")
    
    async def get_security_summary(self) -> Dict[str, Any]:
        """Получение сводки по безопасности"""
        try:
            threat_events = await self.detect_threats()
            
            return {
                "threat_level": threat_events.get("threat_level", "unknown"),
                "failed_logins": threat_events.get("failed_login_attempts", {}).get("total_failed_attempts", 0),
                "suspicious_ips": threat_events.get("suspicious_ip_activity", {}).get("suspicious_ips_count", 0),
                "brute_force_active": threat_events.get("brute_force_attempts", {}).get("is_brute_force_active", False),
                "last_check": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"[Security Monitor] Ошибка получения сводки безопасности: {e}")
            return {"status": "error"}
