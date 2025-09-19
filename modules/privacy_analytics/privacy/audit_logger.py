"""
Система аудита для соблюдения приватности
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

from .. import settings
from logger import logger


class AuditEventType(Enum):
    """Типы событий аудита"""
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    DATA_DELETION = "data_deletion"
    PRIVACY_CHECK = "privacy_check"
    CONSENT_GIVEN = "consent_given"
    CONSENT_WITHDRAWN = "consent_withdrawn"
    DATA_BREACH = "data_breach"
    ADMIN_ACTION = "admin_action"
    USER_ACTION = "user_action"
    SYSTEM_EVENT = "system_event"


class AuditSeverity(Enum):
    """Уровни серьезности событий аудита"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditLogger:
    """Система аудита для соблюдения приватности"""
    
    def __init__(self):
        self.audit_log = []
        self.retention_days = settings.AUDIT_LOG_RETENTION_DAYS
        self.max_log_size = 10000
        
    async def log_event(self, 
                       event_type: AuditEventType,
                       description: str,
                       user_id: Optional[str] = None,
                       resource: Optional[str] = None,
                       severity: AuditSeverity = AuditSeverity.MEDIUM,
                       metadata: Optional[Dict[str, Any]] = None) -> str:
        """Логирование события аудита"""
        try:
            event_id = f"audit_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Анонимизируем пользователя, если указан
            anonymized_user_id = await self._anonymize_user_id(user_id) if user_id else None
            
            event = {
                "id": event_id,
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": event_type.value,
                "description": description,
                "user_id": anonymized_user_id,
                "resource": resource,
                "severity": severity.value,
                "metadata": metadata or {},
                "ip_address": "***.***.***.***",  # Анонимизированный IP
                "user_agent": "***",  # Анонимизированный User-Agent
                "session_id": "***"  # Анонимизированный Session ID
            }
            
            # Добавляем хеш для целостности
            event["integrity_hash"] = await self._calculate_integrity_hash(event)
            
            self.audit_log.append(event)
            
            # Ограничиваем размер лога
            if len(self.audit_log) > self.max_log_size:
                self.audit_log = self.audit_log[-self.max_log_size//2:]
            
            # Логируем в основной лог
            logger.info(f"[Audit] {event_type.value}: {description}")
            
            return event_id
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования события: {e}")
            return ""
    
    async def log_data_access(self, 
                             resource: str,
                             user_id: Optional[str] = None,
                             data_categories: Optional[List[str]] = None,
                             purpose: Optional[str] = None) -> str:
        """Логирование доступа к данным"""
        try:
            description = f"Доступ к ресурсу: {resource}"
            if data_categories:
                description += f", категории данных: {', '.join(data_categories)}"
            if purpose:
                description += f", цель: {purpose}"
            
            metadata = {
                "resource": resource,
                "data_categories": data_categories or [],
                "purpose": purpose,
                "access_method": "api",
                "data_volume": "unknown"
            }
            
            return await self.log_event(
                event_type=AuditEventType.DATA_ACCESS,
                description=description,
                user_id=user_id,
                resource=resource,
                severity=AuditSeverity.MEDIUM,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования доступа к данным: {e}")
            return ""
    
    async def log_data_modification(self, 
                                   resource: str,
                                   user_id: Optional[str] = None,
                                   changes: Optional[Dict[str, Any]] = None) -> str:
        """Логирование изменения данных"""
        try:
            description = f"Изменение ресурса: {resource}"
            if changes:
                description += f", изменений: {len(changes)}"
            
            metadata = {
                "resource": resource,
                "changes": changes or {},
                "change_type": "update",
                "backup_created": True
            }
            
            return await self.log_event(
                event_type=AuditEventType.DATA_MODIFICATION,
                description=description,
                user_id=user_id,
                resource=resource,
                severity=AuditSeverity.HIGH,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования изменения данных: {e}")
            return ""
    
    async def log_data_deletion(self, 
                               resource: str,
                               user_id: Optional[str] = None,
                               data_categories: Optional[List[str]] = None) -> str:
        """Логирование удаления данных"""
        try:
            description = f"Удаление ресурса: {resource}"
            if data_categories:
                description += f", категории данных: {', '.join(data_categories)}"
            
            metadata = {
                "resource": resource,
                "data_categories": data_categories or [],
                "deletion_method": "soft_delete",
                "backup_available": True
            }
            
            return await self.log_event(
                event_type=AuditEventType.DATA_DELETION,
                description=description,
                user_id=user_id,
                resource=resource,
                severity=AuditSeverity.HIGH,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования удаления данных: {e}")
            return ""
    
    async def log_privacy_check(self, 
                               data_hash: str,
                               compliance_result: bool,
                               privacy_level: str,
                               violations: Optional[List[str]] = None) -> str:
        """Логирование проверки приватности"""
        try:
            description = f"Проверка приватности: {'соответствует' if compliance_result else 'нарушения обнаружены'}"
            if violations:
                description += f", нарушений: {len(violations)}"
            
            metadata = {
                "data_hash": data_hash,
                "compliance_result": compliance_result,
                "privacy_level": privacy_level,
                "violations": violations or [],
                "check_method": "automated"
            }
            
            return await self.log_event(
                event_type=AuditEventType.PRIVACY_CHECK,
                description=description,
                severity=AuditSeverity.HIGH if not compliance_result else AuditSeverity.LOW,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования проверки приватности: {e}")
            return ""
    
    async def log_consent_given(self, 
                               subject_id: str,
                               purpose: str,
                               consent_method: str = "explicit") -> str:
        """Логирование предоставления согласия"""
        try:
            description = f"Согласие предоставлено субъектом {subject_id} для цели: {purpose}"
            
            metadata = {
                "subject_id": subject_id,
                "purpose": purpose,
                "consent_method": consent_method,
                "consent_timestamp": datetime.utcnow().isoformat(),
                "withdrawable": True
            }
            
            return await self.log_event(
                event_type=AuditEventType.CONSENT_GIVEN,
                description=description,
                user_id=subject_id,
                severity=AuditSeverity.MEDIUM,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования согласия: {e}")
            return ""
    
    async def log_consent_withdrawn(self, 
                                   subject_id: str,
                                   purpose: str,
                                   withdrawal_method: str = "explicit") -> str:
        """Логирование отзыва согласия"""
        try:
            description = f"Согласие отозвано субъектом {subject_id} для цели: {purpose}"
            
            metadata = {
                "subject_id": subject_id,
                "purpose": purpose,
                "withdrawal_method": withdrawal_method,
                "withdrawal_timestamp": datetime.utcnow().isoformat(),
                "data_retention_updated": True
            }
            
            return await self.log_event(
                event_type=AuditEventType.CONSENT_WITHDRAWN,
                description=description,
                user_id=subject_id,
                severity=AuditSeverity.HIGH,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования отзыва согласия: {e}")
            return ""
    
    async def log_data_breach(self, 
                             description: str,
                             affected_subjects: int,
                             data_categories: Optional[List[str]] = None,
                             severity: AuditSeverity = AuditSeverity.HIGH) -> str:
        """Логирование нарушения данных"""
        try:
            full_description = f"Нарушение данных: {description}, затронуто субъектов: {affected_subjects}"
            
            metadata = {
                "breach_description": description,
                "affected_subjects": affected_subjects,
                "data_categories": data_categories or [],
                "breach_timestamp": datetime.utcnow().isoformat(),
                "reported_to_authorities": False,
                "notified_subjects": False
            }
            
            return await self.log_event(
                event_type=AuditEventType.DATA_BREACH,
                description=full_description,
                severity=severity,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования нарушения данных: {e}")
            return ""
    
    async def log_admin_action(self, 
                              action: str,
                              admin_id: str,
                              target_resource: Optional[str] = None,
                              changes: Optional[Dict[str, Any]] = None) -> str:
        """Логирование административных действий"""
        try:
            description = f"Административное действие: {action}"
            if target_resource:
                description += f", ресурс: {target_resource}"
            
            metadata = {
                "action": action,
                "admin_id": admin_id,
                "target_resource": target_resource,
                "changes": changes or {},
                "action_timestamp": datetime.utcnow().isoformat()
            }
            
            return await self.log_event(
                event_type=AuditEventType.ADMIN_ACTION,
                description=description,
                user_id=admin_id,
                resource=target_resource,
                severity=AuditSeverity.HIGH,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования административного действия: {e}")
            return ""
    
    async def log_user_action(self, 
                             action: str,
                             user_id: str,
                             resource: Optional[str] = None,
                             metadata: Optional[Dict[str, Any]] = None) -> str:
        """Логирование действий пользователя"""
        try:
            description = f"Действие пользователя: {action}"
            if resource:
                description += f", ресурс: {resource}"
            
            action_metadata = {
                "action": action,
                "user_id": user_id,
                "resource": resource,
                "action_timestamp": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
            
            return await self.log_event(
                event_type=AuditEventType.USER_ACTION,
                description=description,
                user_id=user_id,
                resource=resource,
                severity=AuditSeverity.MEDIUM,
                metadata=action_metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования действия пользователя: {e}")
            return ""
    
    async def log_system_event(self, 
                              event: str,
                              component: str,
                              severity: AuditSeverity = AuditSeverity.MEDIUM,
                              metadata: Optional[Dict[str, Any]] = None) -> str:
        """Логирование системных событий"""
        try:
            description = f"Системное событие: {event}, компонент: {component}"
            
            event_metadata = {
                "event": event,
                "component": component,
                "event_timestamp": datetime.utcnow().isoformat(),
                "system_version": "1.0.0",
                **(metadata or {})
            }
            
            return await self.log_event(
                event_type=AuditEventType.SYSTEM_EVENT,
                description=description,
                severity=severity,
                metadata=event_metadata
            )
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка логирования системного события: {e}")
            return ""
    
    async def _anonymize_user_id(self, user_id: str) -> str:
        """Анонимизация ID пользователя"""
        try:
            # Создаем детерминированный анонимный ID
            hash_object = hashlib.sha256((user_id + "audit_salt").encode())
            return f"user_{hash_object.hexdigest()[:12]}"
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка анонимизации ID пользователя: {e}")
            return "anonymous_user"
    
    async def _calculate_integrity_hash(self, event: Dict[str, Any]) -> str:
        """Расчет хеша целостности события"""
        try:
            # Создаем копию события без хеша
            event_copy = event.copy()
            event_copy.pop("integrity_hash", None)
            
            # Сортируем ключи для детерминированного хеша
            sorted_event = json.dumps(event_copy, sort_keys=True, ensure_ascii=False)
            
            # Создаем хеш
            hash_object = hashlib.sha256(sorted_event.encode())
            return hash_object.hexdigest()
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка расчета хеша целостности: {e}")
            return ""
    
    async def get_audit_log(self, 
                           event_type: Optional[AuditEventType] = None,
                           severity: Optional[AuditSeverity] = None,
                           user_id: Optional[str] = None,
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None,
                           limit: int = 100) -> List[Dict[str, Any]]:
        """Получение лога аудита с фильтрацией"""
        try:
            filtered_log = self.audit_log.copy()
            
            # Фильтр по типу события
            if event_type:
                filtered_log = [event for event in filtered_log if event["event_type"] == event_type.value]
            
            # Фильтр по серьезности
            if severity:
                filtered_log = [event for event in filtered_log if event["severity"] == severity.value]
            
            # Фильтр по пользователю
            if user_id:
                anonymized_user_id = await self._anonymize_user_id(user_id)
                filtered_log = [event for event in filtered_log if event.get("user_id") == anonymized_user_id]
            
            # Фильтр по дате
            if start_date:
                filtered_log = [event for event in filtered_log if datetime.fromisoformat(event["timestamp"]) >= start_date]
            
            if end_date:
                filtered_log = [event for event in filtered_log if datetime.fromisoformat(event["timestamp"]) <= end_date]
            
            # Сортируем по времени (новые сначала)
            filtered_log.sort(key=lambda x: x["timestamp"], reverse=True)
            
            # Ограничиваем количество
            return filtered_log[:limit]
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка получения лога аудита: {e}")
            return []
    
    async def get_audit_statistics(self) -> Dict[str, Any]:
        """Получение статистики аудита"""
        try:
            total_events = len(self.audit_log)
            
            # Статистика по типам событий
            event_type_stats = {}
            for event in self.audit_log:
                event_type = event["event_type"]
                event_type_stats[event_type] = event_type_stats.get(event_type, 0) + 1
            
            # Статистика по серьезности
            severity_stats = {}
            for event in self.audit_log:
                severity = event["severity"]
                severity_stats[severity] = severity_stats.get(severity, 0) + 1
            
            # Статистика за последние 24 часа
            last_24h = datetime.utcnow() - timedelta(hours=24)
            recent_events = [
                event for event in self.audit_log
                if datetime.fromisoformat(event["timestamp"]) > last_24h
            ]
            
            # Статистика по пользователям
            user_stats = {}
            for event in self.audit_log:
                user_id = event.get("user_id")
                if user_id:
                    user_stats[user_id] = user_stats.get(user_id, 0) + 1
            
            return {
                "total_events": total_events,
                "events_24h": len(recent_events),
                "event_type_distribution": event_type_stats,
                "severity_distribution": severity_stats,
                "unique_users": len(user_stats),
                "most_active_users": sorted(user_stats.items(), key=lambda x: x[1], reverse=True)[:10],
                "last_event": self.audit_log[-1]["timestamp"] if self.audit_log else None
            }
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка получения статистики: {e}")
            return {}
    
    async def cleanup_old_logs(self):
        """Очистка старых логов"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
            
            # Удаляем старые записи
            self.audit_log = [
                event for event in self.audit_log
                if datetime.fromisoformat(event["timestamp"]) > cutoff_date
            ]
            
            logger.info(f"[Audit Logger] Очищено {len(self.audit_log)} записей аудита")
            
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка очистки старых логов: {e}")
    
    async def export_audit_log(self, 
                              start_date: Optional[datetime] = None,
                              end_date: Optional[datetime] = None,
                              format: str = "json") -> str:
        """Экспорт лога аудита"""
        try:
            # Получаем отфильтрованный лог
            filtered_log = await self.get_audit_log(
                start_date=start_date,
                end_date=end_date,
                limit=10000  # Максимум 10000 записей
            )
            
            if format == "json":
                return json.dumps(filtered_log, ensure_ascii=False, indent=2)
            elif format == "csv":
                # В реальной реализации здесь должна быть конвертация в CSV
                return "CSV export not implemented"
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"[Audit Logger] Ошибка экспорта лога: {e}")
            return ""
