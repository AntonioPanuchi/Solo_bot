"""
Система управления политикой приватности
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import json

from .. import settings
from logger import logger


class PrivacyLevel(Enum):
    """Уровни приватности"""
    MINIMAL = "minimal"  # Минимальная приватность
    STANDARD = "standard"  # Стандартная приватность
    HIGH = "high"  # Высокая приватность
    MAXIMUM = "maximum"  # Максимальная приватность


class DataSubject(Enum):
    """Субъекты данных"""
    USER = "user"
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    VISITOR = "visitor"
    PARTNER = "partner"
    VENDOR = "vendor"


class LegalBasis(Enum):
    """Правовые основания"""
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"


class PrivacyPolicyManager:
    """Система управления политикой приватности"""
    
    def __init__(self):
        self.privacy_policies = self._load_privacy_policies()
        self.data_categories = self._load_data_categories()
        self.processing_purposes = self._load_processing_purposes()
        self.privacy_settings = self._load_privacy_settings()
        self.policy_updates = []  # История обновлений политик
        
    def _load_privacy_policies(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка политик приватности"""
        return {
            "default": {
                "name": "Основная политика приватности",
                "version": "1.0",
                "effective_date": "2024-01-01",
                "privacy_level": PrivacyLevel.STANDARD.value,
                "data_categories": [
                    "personal_data",
                    "technical_data",
                    "analytics_data"
                ],
                "processing_purposes": [
                    "service_provision",
                    "analytics",
                    "security"
                ],
                "legal_basis": LegalBasis.CONSENT.value,
                "retention_period": 365,  # дней
                "anonymization_required": True,
                "encryption_required": True,
                "data_sharing": {
                    "third_parties": False,
                    "international_transfers": False,
                    "government_access": "with_warrant"
                },
                "user_rights": [
                    "access",
                    "rectification",
                    "erasure",
                    "portability",
                    "objection"
                ],
                "contact_info": {
                    "dpo_email": "dpo@example.com",
                    "privacy_email": "privacy@example.com",
                    "phone": "+1-555-0123"
                }
            },
            "analytics": {
                "name": "Политика аналитики",
                "version": "1.0",
                "effective_date": "2024-01-01",
                "privacy_level": PrivacyLevel.HIGH.value,
                "data_categories": [
                    "analytics_data",
                    "usage_data"
                ],
                "processing_purposes": [
                    "analytics",
                    "performance_optimization"
                ],
                "legal_basis": LegalBasis.CONSENT.value,
                "retention_period": 730,  # дней
                "anonymization_required": True,
                "encryption_required": False,
                "data_sharing": {
                    "third_parties": True,
                    "international_transfers": True,
                    "government_access": "with_warrant"
                },
                "user_rights": [
                    "access",
                    "erasure",
                    "objection"
                ],
                "contact_info": {
                    "dpo_email": "dpo@example.com",
                    "privacy_email": "privacy@example.com"
                }
            },
            "security": {
                "name": "Политика безопасности",
                "version": "1.0",
                "effective_date": "2024-01-01",
                "privacy_level": PrivacyLevel.MAXIMUM.value,
                "data_categories": [
                    "security_data",
                    "audit_data"
                ],
                "processing_purposes": [
                    "security",
                    "fraud_prevention"
                ],
                "legal_basis": LegalBasis.LEGITIMATE_INTERESTS.value,
                "retention_period": 2555,  # дней (7 лет)
                "anonymization_required": False,
                "encryption_required": True,
                "data_sharing": {
                    "third_parties": False,
                    "international_transfers": False,
                    "government_access": "with_warrant"
                },
                "user_rights": [
                    "access"
                ],
                "contact_info": {
                    "dpo_email": "dpo@example.com",
                    "security_email": "security@example.com"
                }
            }
        }
    
    def _load_data_categories(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка категорий данных"""
        return {
            "personal_data": {
                "name": "Персональные данные",
                "description": "Данные, которые могут идентифицировать физическое лицо",
                "sensitivity": "high",
                "examples": ["имя", "email", "телефон", "адрес"],
                "protection_level": "maximum"
            },
            "sensitive_data": {
                "name": "Чувствительные данные",
                "description": "Специальные категории персональных данных",
                "sensitivity": "maximum",
                "examples": ["биометрические данные", "религиозные убеждения", "политические взгляды"],
                "protection_level": "maximum"
            },
            "technical_data": {
                "name": "Технические данные",
                "description": "Данные о технических характеристиках и производительности",
                "sensitivity": "low",
                "examples": ["IP-адрес", "User-Agent", "время запроса"],
                "protection_level": "standard"
            },
            "analytics_data": {
                "name": "Аналитические данные",
                "description": "Данные для анализа и улучшения сервиса",
                "sensitivity": "medium",
                "examples": ["статистика использования", "метрики производительности"],
                "protection_level": "high"
            },
            "log_data": {
                "name": "Данные логов",
                "description": "Записи о событиях и операциях в системе",
                "sensitivity": "medium",
                "examples": ["логи доступа", "логи ошибок", "логи транзакций"],
                "protection_level": "standard"
            },
            "audit_data": {
                "name": "Данные аудита",
                "description": "Данные для аудита и соответствия требованиям",
                "sensitivity": "high",
                "examples": ["записи аудита", "доказательства соответствия"],
                "protection_level": "maximum"
            }
        }
    
    def _load_processing_purposes(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка целей обработки"""
        return {
            "service_provision": {
                "name": "Предоставление услуги",
                "description": "Обработка данных для предоставления основной услуги",
                "legal_basis": LegalBasis.CONTRACT.value,
                "retention_period": 365,
                "anonymization_required": False
            },
            "analytics": {
                "name": "Аналитика",
                "description": "Анализ данных для улучшения сервиса",
                "legal_basis": LegalBasis.CONSENT.value,
                "retention_period": 730,
                "anonymization_required": True
            },
            "security": {
                "name": "Безопасность",
                "description": "Обеспечение безопасности и предотвращение мошенничества",
                "legal_basis": LegalBasis.LEGITIMATE_INTERESTS.value,
                "retention_period": 180,
                "anonymization_required": False
            },
            "marketing": {
                "name": "Маркетинг",
                "description": "Маркетинговые коммуникации и реклама",
                "legal_basis": LegalBasis.CONSENT.value,
                "retention_period": 365,
                "anonymization_required": True
            },
            "research": {
                "name": "Исследования",
                "description": "Научные исследования и разработки",
                "legal_basis": LegalBasis.CONSENT.value,
                "retention_period": 1095,
                "anonymization_required": True
            }
        }
    
    def _load_privacy_settings(self) -> Dict[str, Any]:
        """Загрузка настроек приватности"""
        return {
            "default_privacy_level": PrivacyLevel.STANDARD.value,
            "require_explicit_consent": True,
            "allow_implicit_consent": False,
            "data_minimization": True,
            "purpose_limitation": True,
            "storage_limitation": True,
            "accuracy_requirement": True,
            "confidentiality_requirement": True,
            "accountability_requirement": True,
            "transparency_requirement": True,
            "user_control": True,
            "data_portability": True,
            "right_to_be_forgotten": True,
            "privacy_by_design": True,
            "privacy_by_default": True
        }
    
    async def get_privacy_policy(self, 
                                policy_name: str = "default") -> Optional[Dict[str, Any]]:
        """Получение политики приватности"""
        try:
            return self.privacy_policies.get(policy_name)
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка получения политики: {e}")
            return None
    
    async def update_privacy_policy(self, 
                                   policy_name: str,
                                   updates: Dict[str, Any],
                                   reason: str,
                                   updated_by: str) -> bool:
        """Обновление политики приватности"""
        try:
            if policy_name not in self.privacy_policies:
                logger.warning(f"[Privacy Policy] Политика {policy_name} не найдена")
                return False
            
            old_policy = self.privacy_policies[policy_name].copy()
            
            # Обновляем версию
            current_version = old_policy.get("version", "1.0")
            version_parts = current_version.split(".")
            major_version = int(version_parts[0])
            minor_version = int(version_parts[1]) + 1
            new_version = f"{major_version}.{minor_version}"
            
            # Применяем обновления
            self.privacy_policies[policy_name].update(updates)
            self.privacy_policies[policy_name]["version"] = new_version
            self.privacy_policies[policy_name]["last_updated"] = datetime.utcnow().isoformat()
            self.privacy_policies[policy_name]["updated_by"] = updated_by
            
            # Записываем в историю
            self.policy_updates.append({
                "policy_name": policy_name,
                "old_version": current_version,
                "new_version": new_version,
                "updates": updates,
                "reason": reason,
                "updated_by": updated_by,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            logger.info(f"[Privacy Policy] Политика {policy_name} обновлена до версии {new_version}")
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка обновления политики: {e}")
            return False
    
    async def create_custom_policy(self, 
                                  policy_name: str,
                                  policy_data: Dict[str, Any],
                                  created_by: str) -> bool:
        """Создание пользовательской политики"""
        try:
            if policy_name in self.privacy_policies:
                logger.warning(f"[Privacy Policy] Политика {policy_name} уже существует")
                return False
            
            # Устанавливаем значения по умолчанию
            policy_data.setdefault("version", "1.0")
            policy_data.setdefault("effective_date", datetime.utcnow().strftime("%Y-%m-%d"))
            policy_data.setdefault("created_by", created_by)
            policy_data.setdefault("created_at", datetime.utcnow().isoformat())
            
            self.privacy_policies[policy_name] = policy_data
            
            # Записываем в историю
            self.policy_updates.append({
                "policy_name": policy_name,
                "action": "created",
                "policy_data": policy_data,
                "created_by": created_by,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            logger.info(f"[Privacy Policy] Создана пользовательская политика {policy_name}")
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка создания политики: {e}")
            return False
    
    async def validate_policy_compliance(self, 
                                       policy_name: str) -> Dict[str, Any]:
        """Проверка соответствия политики требованиям"""
        try:
            if policy_name not in self.privacy_policies:
                return {"compliant": False, "errors": [f"Политика {policy_name} не найдена"]}
            
            policy = self.privacy_policies[policy_name]
            errors = []
            warnings = []
            
            # Проверяем обязательные поля
            required_fields = ["name", "version", "effective_date", "privacy_level"]
            for field in required_fields:
                if field not in policy:
                    errors.append(f"Отсутствует обязательное поле: {field}")
            
            # Проверяем уровни приватности
            if "privacy_level" in policy:
                valid_levels = [level.value for level in PrivacyLevel]
                if policy["privacy_level"] not in valid_levels:
                    errors.append(f"Недопустимый уровень приватности: {policy['privacy_level']}")
            
            # Проверяем правовые основания
            if "legal_basis" in policy:
                valid_basis = [basis.value for basis in LegalBasis]
                if policy["legal_basis"] not in valid_basis:
                    errors.append(f"Недопустимое правовое основание: {policy['legal_basis']}")
            
            # Проверяем категории данных
            if "data_categories" in policy:
                valid_categories = list(self.data_categories.keys())
                for category in policy["data_categories"]:
                    if category not in valid_categories:
                        warnings.append(f"Неизвестная категория данных: {category}")
            
            # Проверяем цели обработки
            if "processing_purposes" in policy:
                valid_purposes = list(self.processing_purposes.keys())
                for purpose in policy["processing_purposes"]:
                    if purpose not in valid_purposes:
                        warnings.append(f"Неизвестная цель обработки: {purpose}")
            
            # Проверяем период хранения
            if "retention_period" in policy:
                if not isinstance(policy["retention_period"], int) or policy["retention_period"] < 0:
                    errors.append("Период хранения должен быть положительным числом")
            
            # Проверяем контактную информацию
            if "contact_info" not in policy:
                warnings.append("Отсутствует контактная информация")
            
            return {
                "compliant": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "checked_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка проверки соответствия: {e}")
            return {"compliant": False, "errors": [f"Ошибка проверки: {e}"]}
    
    async def get_data_category_info(self, 
                                   category_name: str) -> Optional[Dict[str, Any]]:
        """Получение информации о категории данных"""
        try:
            return self.data_categories.get(category_name)
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка получения категории данных: {e}")
            return None
    
    async def get_processing_purpose_info(self, 
                                        purpose_name: str) -> Optional[Dict[str, Any]]:
        """Получение информации о цели обработки"""
        try:
            return self.processing_purposes.get(purpose_name)
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка получения цели обработки: {e}")
            return None
    
    async def get_privacy_settings(self) -> Dict[str, Any]:
        """Получение настроек приватности"""
        try:
            return self.privacy_settings.copy()
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка получения настроек: {e}")
            return {}
    
    async def update_privacy_settings(self, 
                                    settings: Dict[str, Any],
                                    updated_by: str) -> bool:
        """Обновление настроек приватности"""
        try:
            # Валидируем настройки
            valid_settings = [
                "default_privacy_level",
                "require_explicit_consent",
                "allow_implicit_consent",
                "data_minimization",
                "purpose_limitation",
                "storage_limitation",
                "accuracy_requirement",
                "confidentiality_requirement",
                "accountability_requirement",
                "transparency_requirement",
                "user_control",
                "data_portability",
                "right_to_be_forgotten",
                "privacy_by_design",
                "privacy_by_default"
            ]
            
            for key in settings:
                if key not in valid_settings:
                    logger.warning(f"[Privacy Policy] Неизвестная настройка: {key}")
                    continue
                
                self.privacy_settings[key] = settings[key]
            
            # Записываем в историю
            self.policy_updates.append({
                "action": "settings_updated",
                "settings": settings,
                "updated_by": updated_by,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            logger.info(f"[Privacy Policy] Настройки приватности обновлены")
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка обновления настроек: {e}")
            return False
    
    async def get_policy_history(self, 
                                policy_name: Optional[str] = None,
                                limit: int = 100) -> List[Dict[str, Any]]:
        """Получение истории изменений политик"""
        try:
            filtered_updates = self.policy_updates.copy()
            
            # Фильтр по названию политики
            if policy_name:
                filtered_updates = [
                    update for update in filtered_updates
                    if update.get("policy_name") == policy_name
                ]
            
            # Сортируем по времени (новые сначала)
            filtered_updates.sort(key=lambda x: x["timestamp"], reverse=True)
            
            # Ограничиваем количество
            return filtered_updates[:limit]
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка получения истории: {e}")
            return []
    
    async def get_privacy_statistics(self) -> Dict[str, Any]:
        """Получение статистики политик приватности"""
        try:
            total_policies = len(self.privacy_policies)
            
            # Статистика по уровням приватности
            privacy_level_stats = {}
            for policy in self.privacy_policies.values():
                level = policy.get("privacy_level", "unknown")
                privacy_level_stats[level] = privacy_level_stats.get(level, 0) + 1
            
            # Статистика по правовым основаниям
            legal_basis_stats = {}
            for policy in self.privacy_policies.values():
                basis = policy.get("legal_basis", "unknown")
                legal_basis_stats[basis] = legal_basis_stats.get(basis, 0) + 1
            
            # Статистика по категориям данных
            category_stats = {}
            for policy in self.privacy_policies.values():
                categories = policy.get("data_categories", [])
                for category in categories:
                    category_stats[category] = category_stats.get(category, 0) + 1
            
            # Статистика по целям обработки
            purpose_stats = {}
            for policy in self.privacy_policies.values():
                purposes = policy.get("processing_purposes", [])
                for purpose in purposes:
                    purpose_stats[purpose] = purpose_stats.get(purpose, 0) + 1
            
            # Статистика обновлений
            total_updates = len(self.policy_updates)
            recent_updates = len([
                update for update in self.policy_updates
                if datetime.fromisoformat(update["timestamp"]) > datetime.utcnow() - timedelta(days=30)
            ])
            
            return {
                "total_policies": total_policies,
                "privacy_level_distribution": privacy_level_stats,
                "legal_basis_distribution": legal_basis_stats,
                "data_category_distribution": category_stats,
                "processing_purpose_distribution": purpose_stats,
                "total_updates": total_updates,
                "recent_updates_30d": recent_updates,
                "last_update": self.policy_updates[-1]["timestamp"] if self.policy_updates else None
            }
            
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка получения статистики: {e}")
            return {}
    
    async def export_policy(self, 
                           policy_name: str,
                           format: str = "json") -> str:
        """Экспорт политики приватности"""
        try:
            if policy_name not in self.privacy_policies:
                return ""
            
            policy = self.privacy_policies[policy_name]
            
            if format == "json":
                return json.dumps(policy, ensure_ascii=False, indent=2)
            elif format == "markdown":
                # В реальной реализации здесь должна быть конвертация в Markdown
                return "Markdown export not implemented"
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            logger.error(f"[Privacy Policy] Ошибка экспорта политики: {e}")
            return ""
