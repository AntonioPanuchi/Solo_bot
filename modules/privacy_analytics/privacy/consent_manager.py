"""
Система управления согласием на обработку данных
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import json

from .. import settings
from logger import logger


class ConsentStatus(Enum):
    """Статусы согласия"""
    GIVEN = "given"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"
    PENDING = "pending"
    REVOKED = "revoked"


class ConsentPurpose(Enum):
    """Цели обработки данных"""
    ANALYTICS = "analytics"
    MONITORING = "monitoring"
    SECURITY = "security"
    BUSINESS_ANALYTICS = "business_analytics"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    CUSTOMER_SUPPORT = "customer_support"
    MARKETING = "marketing"
    RESEARCH = "research"


class ConsentMethod(Enum):
    """Методы получения согласия"""
    EXPLICIT = "explicit"
    IMPLICIT = "implicit"
    OPT_IN = "opt_in"
    OPT_OUT = "opt_out"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"


class ConsentManager:
    """Система управления согласием на обработку данных"""
    
    def __init__(self):
        self.consents: Dict[str, Dict[str, Any]] = {}
        self.consent_templates: Dict[str, Dict[str, Any]] = self._load_consent_templates()
        self.consent_history: List[Dict[str, Any]] = []
        
    def _load_consent_templates(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка шаблонов согласия"""
        return {
            "analytics": {
                "purpose": "Аналитика и мониторинг",
                "description": "Сбор и обработка анонимизированных данных для улучшения качества сервиса",
                "data_categories": ["usage_statistics", "performance_metrics", "error_logs"],
                "retention_period": 365,  # дней
                "required": True,
                "withdrawable": True
            },
            "monitoring": {
                "purpose": "Мониторинг системы",
                "description": "Сбор технических данных для обеспечения стабильности работы",
                "data_categories": ["system_metrics", "server_logs", "performance_data"],
                "retention_period": 90,  # дней
                "required": True,
                "withdrawable": False
            },
            "security": {
                "purpose": "Безопасность",
                "description": "Сбор данных для обеспечения безопасности и предотвращения мошенничества",
                "data_categories": ["security_events", "access_logs", "threat_detection"],
                "retention_period": 180,  # дней
                "required": True,
                "withdrawable": False
            },
            "business_analytics": {
                "purpose": "Бизнес-аналитика",
                "description": "Анализ использования сервиса для улучшения бизнес-процессов",
                "data_categories": ["usage_patterns", "feature_adoption", "user_behavior"],
                "retention_period": 730,  # дней
                "required": False,
                "withdrawable": True
            }
        }
    
    async def create_consent(self, 
                            subject_id: str,
                            purpose: ConsentPurpose,
                            consent_method: ConsentMethod = ConsentMethod.EXPLICIT,
                            metadata: Optional[Dict[str, Any]] = None) -> str:
        """Создание нового согласия"""
        try:
            consent_id = f"consent_{subject_id}_{purpose.value}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            # Получаем шаблон для цели
            template = self.consent_templates.get(purpose.value, {})
            
            consent = {
                "id": consent_id,
                "subject_id": subject_id,
                "purpose": purpose.value,
                "status": ConsentStatus.GIVEN.value,
                "consent_method": consent_method.value,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": None,  # Бессрочное согласие
                "withdrawn_at": None,
                "template": template,
                "metadata": metadata or {},
                "version": "1.0"
            }
            
            # Устанавливаем срок действия, если указан в шаблоне
            if template.get("retention_period"):
                consent["expires_at"] = (datetime.utcnow() + timedelta(days=template["retention_period"])).isoformat()
            
            self.consents[consent_id] = consent
            
            # Добавляем в историю
            self.consent_history.append({
                "action": "created",
                "consent_id": consent_id,
                "subject_id": subject_id,
                "purpose": purpose.value,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata or {}
            })
            
            logger.info(f"[Consent Manager] Создано согласие {consent_id} для субъекта {subject_id}")
            return consent_id
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка создания согласия: {e}")
            return ""
    
    async def withdraw_consent(self, 
                              consent_id: str,
                              reason: Optional[str] = None,
                              metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Отзыв согласия"""
        try:
            if consent_id not in self.consents:
                logger.warning(f"[Consent Manager] Согласие {consent_id} не найдено")
                return False
            
            consent = self.consents[consent_id]
            
            # Проверяем, можно ли отозвать согласие
            if not consent["template"].get("withdrawable", True):
                logger.warning(f"[Consent Manager] Согласие {consent_id} не может быть отозвано")
                return False
            
            # Обновляем статус
            consent["status"] = ConsentStatus.WITHDRAWN.value
            consent["withdrawn_at"] = datetime.utcnow().isoformat()
            consent["withdrawal_reason"] = reason
            consent["withdrawal_metadata"] = metadata or {}
            
            # Добавляем в историю
            self.consent_history.append({
                "action": "withdrawn",
                "consent_id": consent_id,
                "subject_id": consent["subject_id"],
                "purpose": consent["purpose"],
                "reason": reason,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata or {}
            })
            
            logger.info(f"[Consent Manager] Согласие {consent_id} отозвано")
            return True
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка отзыва согласия: {e}")
            return False
    
    async def renew_consent(self, 
                           consent_id: str,
                           new_expiry: Optional[datetime] = None,
                           metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Продление согласия"""
        try:
            if consent_id not in self.consents:
                logger.warning(f"[Consent Manager] Согласие {consent_id} не найдено")
                return False
            
            consent = self.consents[consent_id]
            
            # Обновляем срок действия
            if new_expiry:
                consent["expires_at"] = new_expiry.isoformat()
            else:
                # Продлеваем на стандартный период
                template = consent["template"]
                if template.get("retention_period"):
                    consent["expires_at"] = (datetime.utcnow() + timedelta(days=template["retention_period"])).isoformat()
            
            consent["renewed_at"] = datetime.utcnow().isoformat()
            consent["renewal_metadata"] = metadata or {}
            
            # Добавляем в историю
            self.consent_history.append({
                "action": "renewed",
                "consent_id": consent_id,
                "subject_id": consent["subject_id"],
                "purpose": consent["purpose"],
                "new_expiry": consent["expires_at"],
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": metadata or {}
            })
            
            logger.info(f"[Consent Manager] Согласие {consent_id} продлено")
            return True
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка продления согласия: {e}")
            return False
    
    async def check_consent(self, 
                           subject_id: str,
                           purpose: ConsentPurpose,
                           check_expiry: bool = True) -> bool:
        """Проверка наличия действующего согласия"""
        try:
            current_time = datetime.utcnow()
            
            # Ищем активные согласия для данного субъекта и цели
            active_consents = [
                consent for consent in self.consents.values()
                if (consent["subject_id"] == subject_id and 
                    consent["purpose"] == purpose.value and
                    consent["status"] == ConsentStatus.GIVEN.value)
            ]
            
            if not active_consents:
                return False
            
            # Проверяем срок действия, если требуется
            if check_expiry:
                for consent in active_consents:
                    if consent.get("expires_at"):
                        expiry_date = datetime.fromisoformat(consent["expires_at"])
                        if current_time > expiry_date:
                            # Согласие истекло
                            consent["status"] = ConsentStatus.EXPIRED.value
                            continue
                    return True
            else:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка проверки согласия: {e}")
            return False
    
    async def get_consent_status(self, 
                                subject_id: str,
                                purpose: Optional[ConsentPurpose] = None) -> Dict[str, Any]:
        """Получение статуса согласия"""
        try:
            # Фильтруем согласия по субъекту
            subject_consents = [
                consent for consent in self.consents.values()
                if consent["subject_id"] == subject_id
            ]
            
            # Фильтруем по цели, если указана
            if purpose:
                subject_consents = [
                    consent for consent in subject_consents
                    if consent["purpose"] == purpose.value
                ]
            
            # Группируем по статусам
            status_counts = {}
            for consent in subject_consents:
                status = consent["status"]
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Определяем общий статус
            if ConsentStatus.GIVEN.value in status_counts:
                overall_status = ConsentStatus.GIVEN.value
            elif ConsentStatus.PENDING.value in status_counts:
                overall_status = ConsentStatus.PENDING.value
            elif ConsentStatus.EXPIRED.value in status_counts:
                overall_status = ConsentStatus.EXPIRED.value
            else:
                overall_status = ConsentStatus.WITHDRAWN.value
            
            return {
                "subject_id": subject_id,
                "overall_status": overall_status,
                "status_counts": status_counts,
                "total_consents": len(subject_consents),
                "active_consents": status_counts.get(ConsentStatus.GIVEN.value, 0),
                "expired_consents": status_counts.get(ConsentStatus.EXPIRED.value, 0),
                "withdrawn_consents": status_counts.get(ConsentStatus.WITHDRAWN.value, 0)
            }
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка получения статуса согласия: {e}")
            return {}
    
    async def get_consent_history(self, 
                                 subject_id: Optional[str] = None,
                                 purpose: Optional[ConsentPurpose] = None,
                                 limit: int = 100) -> List[Dict[str, Any]]:
        """Получение истории согласий"""
        try:
            filtered_history = self.consent_history.copy()
            
            # Фильтр по субъекту
            if subject_id:
                filtered_history = [
                    entry for entry in filtered_history
                    if entry["subject_id"] == subject_id
                ]
            
            # Фильтр по цели
            if purpose:
                filtered_history = [
                    entry for entry in filtered_history
                    if entry["purpose"] == purpose.value
                ]
            
            # Сортируем по времени (новые сначала)
            filtered_history.sort(key=lambda x: x["timestamp"], reverse=True)
            
            # Ограничиваем количество
            return filtered_history[:limit]
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка получения истории согласий: {e}")
            return []
    
    async def cleanup_expired_consents(self):
        """Очистка истекших согласий"""
        try:
            current_time = datetime.utcnow()
            expired_count = 0
            
            for consent_id, consent in self.consents.items():
                if (consent["status"] == ConsentStatus.GIVEN.value and 
                    consent.get("expires_at")):
                    
                    expiry_date = datetime.fromisoformat(consent["expires_at"])
                    if current_time > expiry_date:
                        consent["status"] = ConsentStatus.EXPIRED.value
                        expired_count += 1
                        
                        # Добавляем в историю
                        self.consent_history.append({
                            "action": "expired",
                            "consent_id": consent_id,
                            "subject_id": consent["subject_id"],
                            "purpose": consent["purpose"],
                            "timestamp": current_time.isoformat(),
                            "metadata": {}
                        })
            
            logger.info(f"[Consent Manager] Очищено {expired_count} истекших согласий")
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка очистки истекших согласий: {e}")
    
    async def get_consent_statistics(self) -> Dict[str, Any]:
        """Получение статистики согласий"""
        try:
            total_consents = len(self.consents)
            
            # Статистика по статусам
            status_stats = {}
            for consent in self.consents.values():
                status = consent["status"]
                status_stats[status] = status_stats.get(status, 0) + 1
            
            # Статистика по целям
            purpose_stats = {}
            for consent in self.consents.values():
                purpose = consent["purpose"]
                purpose_stats[purpose] = purpose_stats.get(purpose, 0) + 1
            
            # Статистика по методам получения согласия
            method_stats = {}
            for consent in self.consents.values():
                method = consent["consent_method"]
                method_stats[method] = method_stats.get(method, 0) + 1
            
            # Статистика за последние 30 дней
            last_30_days = datetime.utcnow() - timedelta(days=30)
            recent_consents = [
                consent for consent in self.consents.values()
                if datetime.fromisoformat(consent["created_at"]) > last_30_days
            ]
            
            # Статистика по субъектам
            unique_subjects = len(set(consent["subject_id"] for consent in self.consents.values()))
            
            return {
                "total_consents": total_consents,
                "unique_subjects": unique_subjects,
                "consents_30d": len(recent_consents),
                "status_distribution": status_stats,
                "purpose_distribution": purpose_stats,
                "method_distribution": method_stats,
                "withdrawal_rate": status_stats.get(ConsentStatus.WITHDRAWN.value, 0) / max(total_consents, 1) * 100,
                "expiry_rate": status_stats.get(ConsentStatus.EXPIRED.value, 0) / max(total_consents, 1) * 100
            }
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка получения статистики: {e}")
            return {}
    
    async def export_consent_data(self, 
                                 subject_id: Optional[str] = None,
                                 format: str = "json") -> str:
        """Экспорт данных о согласиях"""
        try:
            # Фильтруем согласия
            if subject_id:
                filtered_consents = [
                    consent for consent in self.consents.values()
                    if consent["subject_id"] == subject_id
                ]
            else:
                filtered_consents = list(self.consents.values())
            
            if format == "json":
                return json.dumps(filtered_consents, ensure_ascii=False, indent=2)
            elif format == "csv":
                # В реальной реализации здесь должна быть конвертация в CSV
                return "CSV export not implemented"
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка экспорта данных: {e}")
            return ""
    
    async def validate_consent_compliance(self) -> Dict[str, Any]:
        """Проверка соответствия согласий требованиям"""
        try:
            compliance_issues = []
            
            # Проверяем обязательные согласия
            required_purposes = [
                purpose for purpose, template in self.consent_templates.items()
                if template.get("required", False)
            ]
            
            for purpose in required_purposes:
                # Проверяем, есть ли активные согласия для этой цели
                active_consents = [
                    consent for consent in self.consents.values()
                    if (consent["purpose"] == purpose and 
                        consent["status"] == ConsentStatus.GIVEN.value)
                ]
                
                if not active_consents:
                    compliance_issues.append(f"Отсутствуют обязательные согласия для цели: {purpose}")
            
            # Проверяем истекшие согласия
            current_time = datetime.utcnow()
            expired_consents = [
                consent for consent in self.consents.values()
                if (consent["status"] == ConsentStatus.GIVEN.value and 
                    consent.get("expires_at") and
                    datetime.fromisoformat(consent["expires_at"]) < current_time)
            ]
            
            if expired_consents:
                compliance_issues.append(f"Найдено {len(expired_consents)} истекших согласий")
            
            # Проверяем согласия без срока действия
            indefinite_consents = [
                consent for consent in self.consents.values()
                if (consent["status"] == ConsentStatus.GIVEN.value and 
                    not consent.get("expires_at"))
            ]
            
            if indefinite_consents:
                compliance_issues.append(f"Найдено {len(indefinite_consents)} согласий без срока действия")
            
            return {
                "compliance_score": max(0, 100 - len(compliance_issues) * 10),
                "total_issues": len(compliance_issues),
                "issues": compliance_issues,
                "checked_at": current_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"[Consent Manager] Ошибка проверки соответствия: {e}")
            return {"compliance_score": 0, "total_issues": 1, "issues": [f"Ошибка проверки: {e}"], "checked_at": datetime.utcnow().isoformat()}
