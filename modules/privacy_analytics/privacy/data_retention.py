"""
Система управления хранением данных
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import json

from .. import settings
from logger import logger


class DataCategory(Enum):
    """Категории данных"""
    PERSONAL_DATA = "personal_data"
    SENSITIVE_DATA = "sensitive_data"
    TECHNICAL_DATA = "technical_data"
    ANALYTICS_DATA = "analytics_data"
    LOG_DATA = "log_data"
    AUDIT_DATA = "audit_data"
    CONSENT_DATA = "consent_data"
    BUSINESS_DATA = "business_data"


class RetentionPolicy(Enum):
    """Политики хранения"""
    MINIMUM = "minimum"  # Минимальное хранение
    STANDARD = "standard"  # Стандартное хранение
    EXTENDED = "extended"  # Расширенное хранение
    PERMANENT = "permanent"  # Постоянное хранение
    CUSTOM = "custom"  # Пользовательская политика


class DataRetentionManager:
    """Система управления хранением данных"""
    
    def __init__(self):
        self.retention_policies = self._load_retention_policies()
        self.data_lifecycle = {}  # Отслеживание жизненного цикла данных
        self.retention_events = []  # События управления хранением
        
    def _load_retention_policies(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка политик хранения данных"""
        return {
            "personal_data": {
                "category": DataCategory.PERSONAL_DATA.value,
                "retention_period": 365,  # дней
                "policy": RetentionPolicy.STANDARD.value,
                "anonymization_required": True,
                "encryption_required": True,
                "backup_required": True,
                "deletion_method": "secure_delete",
                "legal_basis": "consent",
                "description": "Персональные данные пользователей"
            },
            "sensitive_data": {
                "category": DataCategory.SENSITIVE_DATA.value,
                "retention_period": 180,  # дней
                "policy": RetentionPolicy.MINIMUM.value,
                "anonymization_required": True,
                "encryption_required": True,
                "backup_required": False,
                "deletion_method": "secure_delete",
                "legal_basis": "legitimate_interest",
                "description": "Чувствительные данные"
            },
            "technical_data": {
                "category": DataCategory.TECHNICAL_DATA.value,
                "retention_period": 90,  # дней
                "policy": RetentionPolicy.MINIMUM.value,
                "anonymization_required": False,
                "encryption_required": False,
                "backup_required": False,
                "deletion_method": "standard_delete",
                "legal_basis": "legitimate_interest",
                "description": "Технические данные системы"
            },
            "analytics_data": {
                "category": DataCategory.ANALYTICS_DATA.value,
                "retention_period": 730,  # дней
                "policy": RetentionPolicy.EXTENDED.value,
                "anonymization_required": True,
                "encryption_required": False,
                "backup_required": True,
                "deletion_method": "standard_delete",
                "legal_basis": "consent",
                "description": "Аналитические данные"
            },
            "log_data": {
                "category": DataCategory.LOG_DATA.value,
                "retention_period": 30,  # дней
                "policy": RetentionPolicy.MINIMUM.value,
                "anonymization_required": True,
                "encryption_required": False,
                "backup_required": False,
                "deletion_method": "standard_delete",
                "legal_basis": "legitimate_interest",
                "description": "Логи системы"
            },
            "audit_data": {
                "category": DataCategory.AUDIT_DATA.value,
                "retention_period": 2555,  # дней (7 лет)
                "policy": RetentionPolicy.EXTENDED.value,
                "anonymization_required": False,
                "encryption_required": True,
                "backup_required": True,
                "deletion_method": "secure_delete",
                "legal_basis": "legal_obligation",
                "description": "Данные аудита"
            },
            "consent_data": {
                "category": DataCategory.CONSENT_DATA.value,
                "retention_period": 2555,  # дней (7 лет)
                "policy": RetentionPolicy.EXTENDED.value,
                "anonymization_required": False,
                "encryption_required": True,
                "backup_required": True,
                "deletion_method": "secure_delete",
                "legal_basis": "legal_obligation",
                "description": "Данные о согласиях"
            },
            "business_data": {
                "category": DataCategory.BUSINESS_DATA.value,
                "retention_period": 1095,  # дней (3 года)
                "policy": RetentionPolicy.STANDARD.value,
                "anonymization_required": True,
                "encryption_required": True,
                "backup_required": True,
                "deletion_method": "secure_delete",
                "legal_basis": "legitimate_interest",
                "description": "Бизнес-данные"
            }
        }
    
    async def register_data(self, 
                           data_id: str,
                           category: DataCategory,
                           data_type: str,
                           size_bytes: int,
                           metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Регистрация данных для отслеживания жизненного цикла"""
        try:
            policy = self.retention_policies.get(category.value, {})
            
            data_entry = {
                "id": data_id,
                "category": category.value,
                "data_type": data_type,
                "size_bytes": size_bytes,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(days=policy.get("retention_period", 365))).isoformat(),
                "policy": policy,
                "status": "active",
                "anonymized": False,
                "encrypted": False,
                "backed_up": False,
                "metadata": metadata or {}
            }
            
            self.data_lifecycle[data_id] = data_entry
            
            # Логируем событие
            await self._log_retention_event("data_registered", data_id, {
                "category": category.value,
                "data_type": data_type,
                "size_bytes": size_bytes,
                "retention_period": policy.get("retention_period", 365)
            })
            
            logger.info(f"[Data Retention] Зарегистрированы данные {data_id} категории {category.value}")
            return True
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка регистрации данных: {e}")
            return False
    
    async def update_data_status(self, 
                                data_id: str,
                                status: str,
                                metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Обновление статуса данных"""
        try:
            if data_id not in self.data_lifecycle:
                logger.warning(f"[Data Retention] Данные {data_id} не найдены")
                return False
            
            old_status = self.data_lifecycle[data_id]["status"]
            self.data_lifecycle[data_id]["status"] = status
            self.data_lifecycle[data_id]["last_updated"] = datetime.utcnow().isoformat()
            
            if metadata:
                self.data_lifecycle[data_id]["metadata"].update(metadata)
            
            # Логируем событие
            await self._log_retention_event("status_updated", data_id, {
                "old_status": old_status,
                "new_status": status,
                "metadata": metadata
            })
            
            logger.info(f"[Data Retention] Статус данных {data_id} изменен с {old_status} на {status}")
            return True
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка обновления статуса: {e}")
            return False
    
    async def mark_data_anonymized(self, 
                                  data_id: str,
                                  anonymization_method: str,
                                  metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Отметка данных как анонимизированных"""
        try:
            if data_id not in self.data_lifecycle:
                logger.warning(f"[Data Retention] Данные {data_id} не найдены")
                return False
            
            self.data_lifecycle[data_id]["anonymized"] = True
            self.data_lifecycle[data_id]["anonymization_method"] = anonymization_method
            self.data_lifecycle[data_id]["anonymized_at"] = datetime.utcnow().isoformat()
            
            if metadata:
                self.data_lifecycle[data_id]["metadata"].update(metadata)
            
            # Логируем событие
            await self._log_retention_event("data_anonymized", data_id, {
                "anonymization_method": anonymization_method,
                "metadata": metadata
            })
            
            logger.info(f"[Data Retention] Данные {data_id} анонимизированы методом {anonymization_method}")
            return True
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка отметки анонимизации: {e}")
            return False
    
    async def mark_data_encrypted(self, 
                                 data_id: str,
                                 encryption_method: str,
                                 metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Отметка данных как зашифрованных"""
        try:
            if data_id not in self.data_lifecycle:
                logger.warning(f"[Data Retention] Данные {data_id} не найдены")
                return False
            
            self.data_lifecycle[data_id]["encrypted"] = True
            self.data_lifecycle[data_id]["encryption_method"] = encryption_method
            self.data_lifecycle[data_id]["encrypted_at"] = datetime.utcnow().isoformat()
            
            if metadata:
                self.data_lifecycle[data_id]["metadata"].update(metadata)
            
            # Логируем событие
            await self._log_retention_event("data_encrypted", data_id, {
                "encryption_method": encryption_method,
                "metadata": metadata
            })
            
            logger.info(f"[Data Retention] Данные {data_id} зашифрованы методом {encryption_method}")
            return True
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка отметки шифрования: {e}")
            return False
    
    async def mark_data_backed_up(self, 
                                 data_id: str,
                                 backup_location: str,
                                 metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Отметка данных как резервно скопированных"""
        try:
            if data_id not in self.data_lifecycle:
                logger.warning(f"[Data Retention] Данные {data_id} не найдены")
                return False
            
            self.data_lifecycle[data_id]["backed_up"] = True
            self.data_lifecycle[data_id]["backup_location"] = backup_location
            self.data_lifecycle[data_id]["backed_up_at"] = datetime.utcnow().isoformat()
            
            if metadata:
                self.data_lifecycle[data_id]["metadata"].update(metadata)
            
            # Логируем событие
            await self._log_retention_event("data_backed_up", data_id, {
                "backup_location": backup_location,
                "metadata": metadata
            })
            
            logger.info(f"[Data Retention] Данные {data_id} скопированы в резервную копию")
            return True
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка отметки резервного копирования: {e}")
            return False
    
    async def check_data_expiry(self) -> List[str]:
        """Проверка истекших данных"""
        try:
            current_time = datetime.utcnow()
            expired_data = []
            
            for data_id, data_entry in self.data_lifecycle.items():
                if data_entry["status"] == "active":
                    expires_at = datetime.fromisoformat(data_entry["expires_at"])
                    if current_time > expires_at:
                        expired_data.append(data_id)
                        data_entry["status"] = "expired"
                        data_entry["expired_at"] = current_time.isoformat()
                        
                        # Логируем событие
                        await self._log_retention_event("data_expired", data_id, {
                            "expires_at": data_entry["expires_at"],
                            "retention_period": data_entry["policy"].get("retention_period", 365)
                        })
            
            if expired_data:
                logger.info(f"[Data Retention] Найдено {len(expired_data)} истекших данных")
            
            return expired_data
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка проверки истечения: {e}")
            return []
    
    async def schedule_data_deletion(self, 
                                   data_id: str,
                                   deletion_method: Optional[str] = None,
                                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Планирование удаления данных"""
        try:
            if data_id not in self.data_lifecycle:
                logger.warning(f"[Data Retention] Данные {data_id} не найдены")
                return False
            
            data_entry = self.data_lifecycle[data_id]
            policy = data_entry["policy"]
            
            # Определяем метод удаления
            if not deletion_method:
                deletion_method = policy.get("deletion_method", "standard_delete")
            
            # Обновляем статус
            data_entry["status"] = "scheduled_for_deletion"
            data_entry["deletion_method"] = deletion_method
            data_entry["scheduled_for_deletion_at"] = datetime.utcnow().isoformat()
            
            if metadata:
                data_entry["metadata"].update(metadata)
            
            # Логируем событие
            await self._log_retention_event("deletion_scheduled", data_id, {
                "deletion_method": deletion_method,
                "metadata": metadata
            })
            
            logger.info(f"[Data Retention] Запланировано удаление данных {data_id} методом {deletion_method}")
            return True
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка планирования удаления: {e}")
            return False
    
    async def delete_data(self, 
                         data_id: str,
                         deletion_method: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Удаление данных"""
        try:
            if data_id not in self.data_lifecycle:
                logger.warning(f"[Data Retention] Данные {data_id} не найдены")
                return False
            
            data_entry = self.data_lifecycle[data_id]
            
            # Определяем метод удаления
            if not deletion_method:
                deletion_method = data_entry.get("deletion_method", "standard_delete")
            
            # Выполняем удаление в зависимости от метода
            if deletion_method == "secure_delete":
                # Безопасное удаление (перезапись данных)
                await self._secure_delete_data(data_id, data_entry)
            else:
                # Стандартное удаление
                await self._standard_delete_data(data_id, data_entry)
            
            # Обновляем статус
            data_entry["status"] = "deleted"
            data_entry["deleted_at"] = datetime.utcnow().isoformat()
            data_entry["deletion_method"] = deletion_method
            
            if metadata:
                data_entry["metadata"].update(metadata)
            
            # Логируем событие
            await self._log_retention_event("data_deleted", data_id, {
                "deletion_method": deletion_method,
                "metadata": metadata
            })
            
            logger.info(f"[Data Retention] Данные {data_id} удалены методом {deletion_method}")
            return True
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка удаления данных: {e}")
            return False
    
    async def _secure_delete_data(self, data_id: str, data_entry: Dict[str, Any]):
        """Безопасное удаление данных"""
        try:
            # В реальной реализации здесь должна быть перезапись данных
            # Для демонстрации просто логируем
            logger.info(f"[Data Retention] Выполняется безопасное удаление данных {data_id}")
            
            # Симуляция перезаписи
            await asyncio.sleep(0.1)
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка безопасного удаления: {e}")
    
    async def _standard_delete_data(self, data_id: str, data_entry: Dict[str, Any]):
        """Стандартное удаление данных"""
        try:
            # В реальной реализации здесь должно быть удаление данных
            # Для демонстрации просто логируем
            logger.info(f"[Data Retention] Выполняется стандартное удаление данных {data_id}")
            
            # Симуляция удаления
            await asyncio.sleep(0.1)
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка стандартного удаления: {e}")
    
    async def get_data_lifecycle(self, 
                                data_id: str) -> Optional[Dict[str, Any]]:
        """Получение информации о жизненном цикле данных"""
        try:
            return self.data_lifecycle.get(data_id)
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка получения жизненного цикла: {e}")
            return None
    
    async def get_expired_data(self) -> List[Dict[str, Any]]:
        """Получение списка истекших данных"""
        try:
            current_time = datetime.utcnow()
            expired_data = []
            
            for data_id, data_entry in self.data_lifecycle.items():
                if data_entry["status"] == "active":
                    expires_at = datetime.fromisoformat(data_entry["expires_at"])
                    if current_time > expires_at:
                        expired_data.append(data_entry)
            
            return expired_data
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка получения истекших данных: {e}")
            return []
    
    async def get_retention_statistics(self) -> Dict[str, Any]:
        """Получение статистики хранения данных"""
        try:
            total_data = len(self.data_lifecycle)
            
            # Статистика по статусам
            status_stats = {}
            for data_entry in self.data_lifecycle.values():
                status = data_entry["status"]
                status_stats[status] = status_stats.get(status, 0) + 1
            
            # Статистика по категориям
            category_stats = {}
            for data_entry in self.data_lifecycle.values():
                category = data_entry["category"]
                category_stats[category] = category_stats.get(category, 0) + 1
            
            # Статистика по политикам
            policy_stats = {}
            for data_entry in self.data_lifecycle.values():
                policy = data_entry["policy"].get("policy", "unknown")
                policy_stats[policy] = policy_stats.get(policy, 0) + 1
            
            # Статистика по размерам
            total_size = sum(data_entry["size_bytes"] for data_entry in self.data_lifecycle.values())
            
            # Статистика по анонимизации и шифрованию
            anonymized_count = sum(1 for data_entry in self.data_lifecycle.values() if data_entry.get("anonymized", False))
            encrypted_count = sum(1 for data_entry in self.data_lifecycle.values() if data_entry.get("encrypted", False))
            backed_up_count = sum(1 for data_entry in self.data_lifecycle.values() if data_entry.get("backed_up", False))
            
            return {
                "total_data_entries": total_data,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "status_distribution": status_stats,
                "category_distribution": category_stats,
                "policy_distribution": policy_stats,
                "anonymized_data": anonymized_count,
                "encrypted_data": encrypted_count,
                "backed_up_data": backed_up_count,
                "anonymization_rate": round(anonymized_count / max(total_data, 1) * 100, 2),
                "encryption_rate": round(encrypted_count / max(total_data, 1) * 100, 2),
                "backup_rate": round(backed_up_count / max(total_data, 1) * 100, 2)
            }
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка получения статистики: {e}")
            return {}
    
    async def cleanup_old_data(self):
        """Очистка старых данных"""
        try:
            # Удаляем данные, которые были удалены более 30 дней назад
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            deleted_data = [
                data_id for data_id, data_entry in self.data_lifecycle.items()
                if (data_entry["status"] == "deleted" and 
                    data_entry.get("deleted_at") and
                    datetime.fromisoformat(data_entry["deleted_at"]) < cutoff_date)
            ]
            
            for data_id in deleted_data:
                del self.data_lifecycle[data_id]
            
            logger.info(f"[Data Retention] Очищено {len(deleted_data)} старых записей")
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка очистки старых данных: {e}")
    
    async def _log_retention_event(self, 
                                  event_type: str,
                                  data_id: str,
                                  metadata: Dict[str, Any]):
        """Логирование события управления хранением"""
        try:
            event = {
                "event_type": event_type,
                "data_id": data_id,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata
            }
            
            self.retention_events.append(event)
            
            # Ограничиваем размер лога событий
            if len(self.retention_events) > 10000:
                self.retention_events = self.retention_events[-5000:]
                
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка логирования события: {e}")
    
    async def get_retention_events(self, 
                                  event_type: Optional[str] = None,
                                  data_id: Optional[str] = None,
                                  limit: int = 100) -> List[Dict[str, Any]]:
        """Получение событий управления хранением"""
        try:
            filtered_events = self.retention_events.copy()
            
            # Фильтр по типу события
            if event_type:
                filtered_events = [
                    event for event in filtered_events
                    if event["event_type"] == event_type
                ]
            
            # Фильтр по ID данных
            if data_id:
                filtered_events = [
                    event for event in filtered_events
                    if event["data_id"] == data_id
                ]
            
            # Сортируем по времени (новые сначала)
            filtered_events.sort(key=lambda x: x["timestamp"], reverse=True)
            
            # Ограничиваем количество
            return filtered_events[:limit]
            
        except Exception as e:
            logger.error(f"[Data Retention] Ошибка получения событий: {e}")
            return []
