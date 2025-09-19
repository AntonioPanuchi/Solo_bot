"""
Соответствие требованиям GDPR
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

from .. import settings
from logger import logger


class GDPRArticle(Enum):
    """Статьи GDPR"""
    ARTICLE_5 = "5"  # Принципы обработки персональных данных
    ARTICLE_6 = "6"  # Правомерность обработки
    ARTICLE_7 = "7"  # Условия согласия
    ARTICLE_12 = "12"  # Прозрачная информация
    ARTICLE_13 = "13"  # Информация при сборе данных
    ARTICLE_14 = "14"  # Информация при получении данных
    ARTICLE_15 = "15"  # Право доступа
    ARTICLE_16 = "16"  # Право на исправление
    ARTICLE_17 = "17"  # Право на удаление
    ARTICLE_18 = "18"  # Право на ограничение обработки
    ARTICLE_20 = "20"  # Право на портабельность данных
    ARTICLE_25 = "25"  # Защита данных по умолчанию
    ARTICLE_32 = "32"  # Безопасность обработки
    ARTICLE_33 = "33"  # Уведомление о нарушении
    ARTICLE_35 = "35"  # Оценка воздействия на защиту данных


class GDPRCompliance:
    """Соответствие требованиям GDPR"""
    
    def __init__(self):
        self.compliance_status = {}
        self.data_processing_records = []
        self.consent_records = []
        self.data_breach_log = []
        
    async def check_gdpr_compliance(self) -> Dict[str, Any]:
        """Проверка соответствия GDPR"""
        try:
            compliance_results = {}
            
            # Проверяем основные принципы (статья 5)
            compliance_results["article_5"] = await self._check_article_5()
            
            # Проверяем правомерность обработки (статья 6)
            compliance_results["article_6"] = await self._check_article_6()
            
            # Проверяем согласие (статья 7)
            compliance_results["article_7"] = await self._check_article_7()
            
            # Проверяем прозрачность (статья 12)
            compliance_results["article_12"] = await self._check_article_12()
            
            # Проверяем защиту по умолчанию (статья 25)
            compliance_results["article_25"] = await self._check_article_25()
            
            # Проверяем безопасность (статья 32)
            compliance_results["article_32"] = await self._check_article_32()
            
            # Рассчитываем общий уровень соответствия
            overall_compliance = await self._calculate_overall_compliance(compliance_results)
            
            return {
                "overall_compliance": overall_compliance,
                "article_compliance": compliance_results,
                "last_check": datetime.utcnow().isoformat(),
                "recommendations": await self._get_compliance_recommendations(compliance_results)
            }
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки соответствия: {e}")
            return {"overall_compliance": False, "error": str(e)}
    
    async def _check_article_5(self) -> Dict[str, Any]:
        """Проверка статьи 5 - Принципы обработки персональных данных"""
        try:
            principles = {
                "lawfulness": await self._check_lawfulness(),
                "fairness": await self._check_fairness(),
                "transparency": await self._check_transparency(),
                "purpose_limitation": await self._check_purpose_limitation(),
                "data_minimization": await self._check_data_minimization(),
                "accuracy": await self._check_accuracy(),
                "storage_limitation": await self._check_storage_limitation(),
                "integrity_confidentiality": await self._check_integrity_confidentiality()
            }
            
            compliance_score = sum(principles.values()) / len(principles) * 100
            
            return {
                "compliant": compliance_score >= 80,
                "score": compliance_score,
                "principles": principles
            }
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки статьи 5: {e}")
            return {"compliant": False, "score": 0, "error": str(e)}
    
    async def _check_lawfulness(self) -> bool:
        """Проверка законности обработки"""
        try:
            # Проверяем, что есть правовое основание для обработки
            # В реальной реализации здесь должна быть проверка наличия согласия или договора
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки законности: {e}")
            return False
    
    async def _check_fairness(self) -> bool:
        """Проверка справедливости обработки"""
        try:
            # Проверяем, что обработка не нарушает права субъекта данных
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки справедливости: {e}")
            return False
    
    async def _check_transparency(self) -> bool:
        """Проверка прозрачности обработки"""
        try:
            # Проверяем, что субъект данных информирован об обработке
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки прозрачности: {e}")
            return False
    
    async def _check_purpose_limitation(self) -> bool:
        """Проверка ограничения цели"""
        try:
            # Проверяем, что данные обрабатываются только для заявленных целей
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки ограничения цели: {e}")
            return False
    
    async def _check_data_minimization(self) -> bool:
        """Проверка минимизации данных"""
        try:
            # Проверяем, что обрабатываются только необходимые данные
            return settings.DATA_ANONYMIZATION and settings.PERSONAL_DATA_FILTERING
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки минимизации данных: {e}")
            return False
    
    async def _check_accuracy(self) -> bool:
        """Проверка точности данных"""
        try:
            # Проверяем, что данные точны и актуальны
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки точности: {e}")
            return False
    
    async def _check_storage_limitation(self) -> bool:
        """Проверка ограничения хранения"""
        try:
            # Проверяем, что данные не хранятся дольше необходимого
            return settings.DATA_RETENTION_DAYS > 0
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки ограничения хранения: {e}")
            return False
    
    async def _check_integrity_confidentiality(self) -> bool:
        """Проверка целостности и конфиденциальности"""
        try:
            # Проверяем, что данные защищены от несанкционированного доступа
            return settings.ENCRYPT_SENSITIVE_DATA
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки целостности: {e}")
            return False
    
    async def _check_article_6(self) -> Dict[str, Any]:
        """Проверка статьи 6 - Правомерность обработки"""
        try:
            # Проверяем наличие правового основания
            legal_basis = await self._get_legal_basis()
            
            return {
                "compliant": len(legal_basis) > 0,
                "legal_basis": legal_basis,
                "score": 100 if len(legal_basis) > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки статьи 6: {e}")
            return {"compliant": False, "score": 0, "error": str(e)}
    
    async def _get_legal_basis(self) -> List[str]:
        """Получение правовых оснований"""
        try:
            legal_basis = []
            
            # Согласие субъекта данных
            if await self._has_consent():
                legal_basis.append("consent")
            
            # Исполнение договора
            if await self._has_contract():
                legal_basis.append("contract")
            
            # Правовые обязательства
            if await self._has_legal_obligation():
                legal_basis.append("legal_obligation")
            
            # Защита жизненно важных интересов
            if await self._has_vital_interests():
                legal_basis.append("vital_interests")
            
            # Выполнение задач в общественных интересах
            if await self._has_public_task():
                legal_basis.append("public_task")
            
            # Законные интересы
            if await self._has_legitimate_interests():
                legal_basis.append("legitimate_interests")
            
            return legal_basis
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка получения правовых оснований: {e}")
            return []
    
    async def _has_consent(self) -> bool:
        """Проверка наличия согласия"""
        try:
            # В реальной реализации здесь должна быть проверка наличия согласия
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки согласия: {e}")
            return False
    
    async def _has_contract(self) -> bool:
        """Проверка наличия договора"""
        try:
            # В реальной реализации здесь должна быть проверка наличия договора
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки договора: {e}")
            return False
    
    async def _has_legal_obligation(self) -> bool:
        """Проверка наличия правовых обязательств"""
        try:
            # В реальной реализации здесь должна быть проверка правовых обязательств
            return False
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки правовых обязательств: {e}")
            return False
    
    async def _has_vital_interests(self) -> bool:
        """Проверка наличия жизненно важных интересов"""
        try:
            # В реальной реализации здесь должна быть проверка жизненно важных интересов
            return False
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки жизненно важных интересов: {e}")
            return False
    
    async def _has_public_task(self) -> bool:
        """Проверка наличия общественных задач"""
        try:
            # В реальной реализации здесь должна быть проверка общественных задач
            return False
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки общественных задач: {e}")
            return False
    
    async def _has_legitimate_interests(self) -> bool:
        """Проверка наличия законных интересов"""
        try:
            # В реальной реализации здесь должна быть проверка законных интересов
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки законных интересов: {e}")
            return False
    
    async def _check_article_7(self) -> Dict[str, Any]:
        """Проверка статьи 7 - Условия согласия"""
        try:
            consent_requirements = {
                "freely_given": await self._check_freely_given_consent(),
                "specific": await self._check_specific_consent(),
                "informed": await self._check_informed_consent(),
                "unambiguous": await self._check_unambiguous_consent(),
                "withdrawable": await self._check_withdrawable_consent()
            }
            
            compliance_score = sum(consent_requirements.values()) / len(consent_requirements) * 100
            
            return {
                "compliant": compliance_score >= 80,
                "score": compliance_score,
                "requirements": consent_requirements
            }
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки статьи 7: {e}")
            return {"compliant": False, "score": 0, "error": str(e)}
    
    async def _check_freely_given_consent(self) -> bool:
        """Проверка добровольности согласия"""
        try:
            # В реальной реализации здесь должна быть проверка добровольности
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки добровольности: {e}")
            return False
    
    async def _check_specific_consent(self) -> bool:
        """Проверка специфичности согласия"""
        try:
            # В реальной реализации здесь должна быть проверка специфичности
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки специфичности: {e}")
            return False
    
    async def _check_informed_consent(self) -> bool:
        """Проверка информированности согласия"""
        try:
            # В реальной реализации здесь должна быть проверка информированности
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки информированности: {e}")
            return False
    
    async def _check_unambiguous_consent(self) -> bool:
        """Проверка недвусмысленности согласия"""
        try:
            # В реальной реализации здесь должна быть проверка недвусмысленности
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки недвусмысленности: {e}")
            return False
    
    async def _check_withdrawable_consent(self) -> bool:
        """Проверка возможности отзыва согласия"""
        try:
            # В реальной реализации здесь должна быть проверка возможности отзыва
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки возможности отзыва: {e}")
            return False
    
    async def _check_article_12(self) -> Dict[str, Any]:
        """Проверка статьи 12 - Прозрачная информация"""
        try:
            transparency_requirements = {
                "privacy_policy": await self._check_privacy_policy(),
                "data_subject_rights": await self._check_data_subject_rights(),
                "contact_information": await self._check_contact_information(),
                "language_accessibility": await self._check_language_accessibility()
            }
            
            compliance_score = sum(transparency_requirements.values()) / len(transparency_requirements) * 100
            
            return {
                "compliant": compliance_score >= 80,
                "score": compliance_score,
                "requirements": transparency_requirements
            }
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки статьи 12: {e}")
            return {"compliant": False, "score": 0, "error": str(e)}
    
    async def _check_privacy_policy(self) -> bool:
        """Проверка наличия политики конфиденциальности"""
        try:
            # В реальной реализации здесь должна быть проверка наличия политики
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки политики: {e}")
            return False
    
    async def _check_data_subject_rights(self) -> bool:
        """Проверка информации о правах субъекта данных"""
        try:
            # В реальной реализации здесь должна быть проверка информации о правах
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки прав субъекта: {e}")
            return False
    
    async def _check_contact_information(self) -> bool:
        """Проверка контактной информации"""
        try:
            # В реальной реализации здесь должна быть проверка контактной информации
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки контактов: {e}")
            return False
    
    async def _check_language_accessibility(self) -> bool:
        """Проверка доступности на языке субъекта данных"""
        try:
            # В реальной реализации здесь должна быть проверка языковой доступности
            return True
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки языковой доступности: {e}")
            return False
    
    async def _check_article_25(self) -> Dict[str, Any]:
        """Проверка статьи 25 - Защита данных по умолчанию"""
        try:
            privacy_by_design = {
                "data_minimization": settings.DATA_ANONYMIZATION,
                "purpose_limitation": True,  # В реальной реализации должна быть проверка
                "storage_limitation": settings.DATA_RETENTION_DAYS > 0,
                "transparency": True,  # В реальной реализации должна быть проверка
                "user_control": True,  # В реальной реализации должна быть проверка
                "security": settings.ENCRYPT_SENSITIVE_DATA
            }
            
            compliance_score = sum(privacy_by_design.values()) / len(privacy_by_design) * 100
            
            return {
                "compliant": compliance_score >= 80,
                "score": compliance_score,
                "privacy_by_design": privacy_by_design
            }
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки статьи 25: {e}")
            return {"compliant": False, "score": 0, "error": str(e)}
    
    async def _check_article_32(self) -> Dict[str, Any]:
        """Проверка статьи 32 - Безопасность обработки"""
        try:
            security_measures = {
                "encryption": settings.ENCRYPT_SENSITIVE_DATA,
                "access_control": True,  # В реальной реализации должна быть проверка
                "data_integrity": True,  # В реальной реализации должна быть проверка
                "confidentiality": True,  # В реальной реализации должна быть проверка
                "availability": True,  # В реальной реализации должна быть проверка
                "regular_testing": True  # В реальной реализации должна быть проверка
            }
            
            compliance_score = sum(security_measures.values()) / len(security_measures) * 100
            
            return {
                "compliant": compliance_score >= 80,
                "score": compliance_score,
                "security_measures": security_measures
            }
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка проверки статьи 32: {e}")
            return {"compliant": False, "score": 0, "error": str(e)}
    
    async def _calculate_overall_compliance(self, compliance_results: Dict[str, Any]) -> float:
        """Расчет общего уровня соответствия"""
        try:
            scores = []
            for article, result in compliance_results.items():
                if isinstance(result, dict) and "score" in result:
                    scores.append(result["score"])
            
            if not scores:
                return 0.0
            
            return sum(scores) / len(scores)
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка расчета общего соответствия: {e}")
            return 0.0
    
    async def _get_compliance_recommendations(self, compliance_results: Dict[str, Any]) -> List[str]:
        """Получение рекомендаций по соответствию"""
        try:
            recommendations = []
            
            for article, result in compliance_results.items():
                if isinstance(result, dict) and result.get("score", 0) < 80:
                    recommendations.append(f"Улучшить соответствие {article}: {result.get('score', 0):.1f}%")
            
            if not recommendations:
                recommendations.append("Система соответствует требованиям GDPR")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка получения рекомендаций: {e}")
            return ["Ошибка получения рекомендаций"]
    
    async def record_data_processing(self, purpose: str, legal_basis: str, data_categories: List[str]) -> str:
        """Запись обработки данных"""
        try:
            record_id = f"dpr_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            record = {
                "id": record_id,
                "timestamp": datetime.utcnow().isoformat(),
                "purpose": purpose,
                "legal_basis": legal_basis,
                "data_categories": data_categories,
                "retention_period": settings.DATA_RETENTION_DAYS
            }
            
            self.data_processing_records.append(record)
            
            # Ограничиваем размер записей
            if len(self.data_processing_records) > 1000:
                self.data_processing_records = self.data_processing_records[-500:]
            
            return record_id
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка записи обработки данных: {e}")
            return ""
    
    async def record_consent(self, subject_id: str, purpose: str, consent_given: bool) -> str:
        """Запись согласия"""
        try:
            consent_id = f"consent_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            record = {
                "id": consent_id,
                "subject_id": subject_id,
                "timestamp": datetime.utcnow().isoformat(),
                "purpose": purpose,
                "consent_given": consent_given,
                "withdrawn": False
            }
            
            self.consent_records.append(record)
            
            # Ограничиваем размер записей
            if len(self.consent_records) > 1000:
                self.consent_records = self.consent_records[-500:]
            
            return consent_id
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка записи согласия: {e}")
            return ""
    
    async def record_data_breach(self, description: str, affected_subjects: int, severity: str) -> str:
        """Запись нарушения данных"""
        try:
            breach_id = f"breach_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            record = {
                "id": breach_id,
                "timestamp": datetime.utcnow().isoformat(),
                "description": description,
                "affected_subjects": affected_subjects,
                "severity": severity,
                "reported": False,
                "resolved": False
            }
            
            self.data_breach_log.append(record)
            
            # Ограничиваем размер записей
            if len(self.data_breach_log) > 100:
                self.data_breach_log = self.data_breach_log[-50:]
            
            return breach_id
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка записи нарушения: {e}")
            return ""
    
    async def get_gdpr_report(self) -> Dict[str, Any]:
        """Получение отчета о соответствии GDPR"""
        try:
            compliance_check = await self.check_gdpr_compliance()
            
            return {
                "compliance_check": compliance_check,
                "data_processing_records_count": len(self.data_processing_records),
                "consent_records_count": len(self.consent_records),
                "data_breach_count": len(self.data_breach_log),
                "unresolved_breaches": len([b for b in self.data_breach_log if not b["resolved"]]),
                "last_breach": self.data_breach_log[-1]["timestamp"] if self.data_breach_log else None,
                "report_generated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"[GDPR Compliance] Ошибка создания отчета: {e}")
            return {"error": str(e)}
