"""
Проверка соответствия требованиям приватности
"""

import re
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from enum import Enum

from .. import settings
from logger import logger


class PrivacyLevel(Enum):
    """Уровни приватности"""
    STRICT = "strict"
    BALANCED = "balanced"
    MINIMAL = "minimal"


class PrivacyComplianceChecker:
    """Проверка соответствия требованиям приватности"""
    
    def __init__(self):
        self.privacy_level = PrivacyLevel(settings.PRIVACY_MODE)
        self.forbidden_patterns = settings.FORBIDDEN_DATA_PATTERNS
        self.personal_data_patterns = self._load_personal_data_patterns()
        self.audit_log = []

    def _load_personal_data_patterns(self) -> List[Dict[str, str]]:
        """Загрузка паттернов персональных данных"""
        return [
            {
                "name": "email",
                "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "description": "Email адреса"
            },
            {
                "name": "phone",
                "pattern": r'(\+7|8)[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}',
                "description": "Номера телефонов"
            },
            {
                "name": "ip_address",
                "pattern": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                "description": "IP адреса"
            },
            {
                "name": "credit_card",
                "pattern": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                "description": "Номера кредитных карт"
            },
            {
                "name": "passport",
                "pattern": r'\b\d{4}\s\d{6}\b',
                "description": "Номера паспортов"
            },
            {
                "name": "inn",
                "pattern": r'\b\d{10}\b|\b\d{12}\b',
                "description": "ИНН"
            },
            {
                "name": "snils",
                "pattern": r'\b\d{3}-\d{3}-\d{3}\s\d{2}\b',
                "description": "СНИЛС"
            }
        ]
    
    async def validate_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Валидация метрик на соответствие требованиям приватности"""
        try:
            # Проверяем наличие запрещенных паттернов
            if not await self._check_forbidden_patterns(metrics):
                return False
            
            # Проверяем персональные данные
            if not await self._check_personal_data(metrics):
                return False
            
            # Проверяем соответствие уровню приватности
            if not await self._check_privacy_level_compliance(metrics):
                return False
            
            # Логируем успешную проверку
            await self._log_privacy_check(metrics, True)
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка валидации метрик: {e}")
            await self._log_privacy_check(metrics, False, str(e))
            return False
    
    async def _check_forbidden_patterns(self, data: Dict[str, Any]) -> bool:
        """Проверка на запрещенные паттерны"""
        try:
            for pattern in self.forbidden_patterns:
                if await self._contains_pattern(data, pattern):
                    logger.warning(f"[Privacy Checker] Обнаружен запрещенный паттерн: {pattern}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки запрещенных паттернов: {e}")
            return False
    
    async def _check_personal_data(self, data: Dict[str, Any]) -> bool:
        """Проверка на персональные данные"""
        try:
            for pattern_info in self.personal_data_patterns:
                if await self._contains_regex_pattern(data, pattern_info["pattern"]):
                    logger.warning(f"[Privacy Checker] Обнаружены персональные данные: {pattern_info['description']}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки персональных данных: {e}")
            return False
    
    async def _check_privacy_level_compliance(self, data: Dict[str, Any]) -> bool:
        """Проверка соответствия уровню приватности"""
        try:
            if self.privacy_level == PrivacyLevel.STRICT:
                return await self._check_strict_privacy(data)
            elif self.privacy_level == PrivacyLevel.BALANCED:
                return await self._check_balanced_privacy(data)
            elif self.privacy_level == PrivacyLevel.MINIMAL:
                return await self._check_minimal_privacy(data)
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки уровня приватности: {e}")
            return False
    
    async def _check_strict_privacy(self, data: Dict[str, Any]) -> bool:
        """Строгая проверка приватности"""
        try:
            # Проверяем на наличие любых идентификаторов
            forbidden_keys = ["user_id", "session_id", "device_id", "client_id"]
            for key in forbidden_keys:
                if await self._contains_key(data, key):
                    logger.warning(f"[Privacy Checker] Строгий режим: обнаружен ключ {key}")
                    return False
            
            # Проверяем на временные метки с высокой точностью
            if await self._has_high_precision_timestamps(data):
                logger.warning("[Privacy Checker] Строгий режим: обнаружены высокоточные временные метки")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка строгой проверки: {e}")
            return False
    
    async def _check_balanced_privacy(self, data: Dict[str, Any]) -> bool:
        """Сбалансированная проверка приватности"""
        try:
            # Разрешаем агрегированные данные
            if await self._is_aggregated_data(data):
                return True
            
            # Проверяем на явные персональные данные
            explicit_personal_data = ["name", "surname", "email", "phone"]
            for key in explicit_personal_data:
                if await self._contains_key(data, key):
                    logger.warning(f"[Privacy Checker] Сбалансированный режим: обнаружен ключ {key}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка сбалансированной проверки: {e}")
            return False
    
    async def _check_minimal_privacy(self, data: Dict[str, Any]) -> bool:
        """Минимальная проверка приватности"""
        try:
            # Проверяем только на явные персональные данные
            explicit_personal_data = ["name", "surname", "email", "phone", "address"]
            for key in explicit_personal_data:
                if await self._contains_key(data, key):
                    logger.warning(f"[Privacy Checker] Минимальный режим: обнаружен ключ {key}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка минимальной проверки: {e}")
            return False
    
    async def _contains_pattern(self, data: Dict[str, Any], pattern: str) -> bool:
        """Проверка наличия паттерна в данных"""
        try:
            return await self._search_in_dict(data, pattern.lower())
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка поиска паттерна {pattern}: {e}")
            return False
    
    async def _contains_regex_pattern(self, data: Dict[str, Any], pattern: str) -> bool:
        """Проверка наличия регулярного выражения в данных"""
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            return await self._search_regex_in_dict(data, regex)
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка поиска regex {pattern}: {e}")
            return False
    
    async def _contains_key(self, data: Dict[str, Any], key: str) -> bool:
        """Проверка наличия ключа в данных"""
        try:
            return await self._search_key_in_dict(data, key.lower())
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка поиска ключа {key}: {e}")
            return False
    
    async def _search_in_dict(self, data: Any, pattern: str) -> bool:
        """Рекурсивный поиск паттерна в словаре"""
        try:
            if isinstance(data, dict):
                for key, value in data.items():
                    if pattern in key.lower() or pattern in str(value).lower():
                        return True
                    if await self._search_in_dict(value, pattern):
                        return True
            elif isinstance(data, list):
                for item in data:
                    if await self._search_in_dict(item, pattern):
                        return True
            elif isinstance(data, str):
                return pattern in data.lower()
            
            return False
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка поиска в словаре: {e}")
            return False
    
    async def _search_regex_in_dict(self, data: Any, regex: re.Pattern) -> bool:
        """Рекурсивный поиск регулярного выражения в словаре"""
        try:
            if isinstance(data, dict):
                for key, value in data.items():
                    # Исключаем технические поля по ключевым словам
                    if any(tech_word in key.lower() for tech_word in [
                        'timestamp', 'time', 'date', 'response', 'request', 'error', 'rate', 'percent',
                        'usage', 'memory', 'cpu', 'disk', 'network', 'connection', 'active', 'users',
                        'database', 'redis', 'api', 'health', 'status', 'load', 'uptime', 'bytes',
                        'count', 'total', 'sum', 'average', 'max', 'min', 'range', 'interval',
                        'duration', 'period', 'metric', 'stat', 'data', 'info', 'config', 'setting',
                        'option', 'param', 'var', 'constant', 'value', 'number', 'count', 'total',
                        'sum', 'average', 'maximum', 'minimum', 'range', 'interval', 'period',
                        'duration', 'time', 'date', 'timestamp', 'epoch', 'unix', 'iso', 'rfc',
                        'utc', 'gmt', 'local', 'timezone', 'offset', 'dst', 'clock', 'timer',
                        'chrono', 'chronometer', 'stopwatch', 'metronome', 'beat', 'rhythm',
                        'cadence', 'tempo', 'pace', 'speed', 'velocity', 'acceleration', 'momentum',
                        'force', 'power', 'energy', 'work', 'effort', 'strain', 'stress', 'tension',
                        'pressure', 'load', 'burden', 'weight', 'mass', 'volume', 'capacity', 'limit',
                        'threshold', 'boundary', 'edge', 'margin', 'room', 'space', 'area', 'zone',
                        'region', 'sector', 'quadrant', 'octant', 'segment', 'section', 'part',
                        'portion', 'fraction', 'percentage', 'ratio', 'proportion', 'scale', 'factor',
                        'multiplier', 'divisor', 'dividend', 'quotient', 'remainder', 'modulo', 'floor',
                        'ceiling', 'round', 'truncate', 'approximate', 'estimate', 'guess', 'approximation',
                        'calculation', 'computation', 'arithmetic', 'math', 'mathematics', 'algebra',
                        'geometry', 'trigonometry', 'calculus', 'statistics', 'probability', 'analytics',
                        'analysis', 'synthesis', 'combination', 'permutation', 'variation', 'server',
                        'system', 'application', 'service', 'process', 'thread', 'task', 'job', 'work',
                        'operation', 'function', 'method', 'procedure', 'routine', 'algorithm', 'logic',
                        'rule', 'condition', 'criteria', 'standard', 'benchmark', 'baseline', 'reference',
                        'target', 'goal', 'objective', 'purpose', 'intent', 'aim', 'scope', 'range',
                        'domain', 'field', 'area', 'category', 'class', 'type', 'kind', 'sort', 'variety',
                        'form', 'format', 'structure', 'pattern', 'model', 'template', 'schema', 'layout',
                        'design', 'architecture', 'framework', 'platform', 'environment', 'context',
                        'situation', 'circumstance', 'condition', 'state', 'status', 'phase', 'stage',
                        'level', 'degree', 'extent', 'scope', 'range', 'span', 'reach', 'coverage',
                        'inclusion', 'exclusion', 'exception', 'special', 'particular', 'specific',
                        'general', 'common', 'standard', 'normal', 'regular', 'typical', 'usual',
                        'ordinary', 'average', 'median', 'mode', 'mean', 'sum', 'total', 'count',
                        'number', 'quantity', 'amount', 'volume', 'size', 'length', 'width', 'height',
                        'depth', 'thickness', 'diameter', 'radius', 'circumference', 'perimeter', 'area',
                        'surface', 'volume', 'capacity', 'density', 'weight', 'mass', 'force', 'pressure',
                        'temperature', 'humidity', 'moisture', 'vapor', 'steam', 'gas', 'liquid', 'solid',
                        'plasma', 'crystal', 'powder', 'dust', 'particle', 'atom', 'molecule', 'ion',
                        'electron', 'proton', 'neutron', 'quark', 'lepton', 'boson', 'fermion', 'photon',
                        'gluon', 'w_boson', 'z_boson', 'higgs', 'graviton', 'tachyon', 'axion', 'neutrino',
                        'muon', 'tau', 'strange', 'charm', 'bottom', 'top', 'up', 'down', 'electron',
                        'muon', 'tau', 'electron_neutrino', 'muon_neutrino', 'tau_neutrino', 'photon',
                        'gluon', 'w_boson', 'z_boson', 'higgs_boson', 'graviton', 'tachyon', 'axion'
                    ]):
                        continue
                    
                    # Исключаем числовые значения (метрики)
                    if isinstance(value, (int, float)):
                        continue
                    
                    # Проверяем только строковые значения
                    if isinstance(value, str) and regex.search(value):
                        return True
                    
                    if await self._search_regex_in_dict(value, regex):
                        return True
            elif isinstance(data, list):
                for item in data:
                    if await self._search_regex_in_dict(item, regex):
                        return True
            elif isinstance(data, str):
                return bool(regex.search(data))
            
            return False
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка поиска regex в словаре: {e}")
            return False
    
    async def _search_key_in_dict(self, data: Any, key: str) -> bool:
        """Рекурсивный поиск ключа в словаре"""
        try:
            if isinstance(data, dict):
                for k, v in data.items():
                    if key in k.lower():
                        return True
                    if await self._search_key_in_dict(v, key):
                        return True
            elif isinstance(data, list):
                for item in data:
                    if await self._search_key_in_dict(item, key):
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка поиска ключа в словаре: {e}")
            return False
    
    async def _is_aggregated_data(self, data: Dict[str, Any]) -> bool:
        """Проверка, являются ли данные агрегированными"""
        try:
            # Проверяем наличие признаков агрегированных данных
            aggregated_indicators = [
                "total", "average", "sum", "count", "max", "min",
                "aggregated", "statistics", "metrics", "summary"
            ]
            
            for indicator in aggregated_indicators:
                if await self._search_in_dict(data, indicator):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки агрегированных данных: {e}")
            return False
    
    async def _has_high_precision_timestamps(self, data: Dict[str, Any]) -> bool:
        """Проверка наличия высокоточных временных меток"""
        try:
            timestamp_keys = ["timestamp", "created_at", "updated_at", "time"]
            
            for key in timestamp_keys:
                if await self._search_key_in_dict(data, key):
                    # Проверяем формат временной метки
                    if await self._check_timestamp_precision(data, key):
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки временных меток: {e}")
            return False
    
    async def _check_timestamp_precision(self, data: Any, key: str) -> bool:
        """Проверка точности временной метки"""
        try:
            if isinstance(data, dict) and key in data:
                timestamp = str(data[key])
                # Проверяем, содержит ли временная метка микросекунды (более 6 цифр после точки)
                if '.' in timestamp and len(timestamp.split('.')[-1]) > 6:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки точности временной метки: {e}")
            return False
    
    async def _log_privacy_check(self, data: Dict[str, Any], success: bool, error: str = None):
        """Логирование проверки приватности"""
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "success": success,
                "privacy_level": self.privacy_level.value,
                "data_hash": hashlib.sha256(str(data).encode()).hexdigest()[:16],
                "error": error
            }
            
            self.audit_log.append(log_entry)
            
            # Ограничиваем размер лога
            if len(self.audit_log) > 1000:
                self.audit_log = self.audit_log[-500:]
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка логирования: {e}")
    
    async def audit_system_compliance(self) -> bool:
        """Аудит соответствия системы требованиям приватности"""
        try:
            # Проверяем настройки приватности
            if not await self._check_privacy_settings():
                return False
            
            # Проверяем логи аудита
            if not await self._check_audit_logs():
                return False
            
            # Проверяем соответствие GDPR
            if not await self._check_gdpr_compliance():
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка аудита соответствия: {e}")
            return False
    
    async def _check_privacy_settings(self) -> bool:
        """Проверка настроек приватности"""
        try:
            # Проверяем, что анонимизация данных включена
            if not settings.DATA_ANONYMIZATION:
                logger.warning("[Privacy Checker] Анонимизация данных отключена")
                return False
            
            # Проверяем, что фильтрация персональных данных включена
            if not settings.PERSONAL_DATA_FILTERING:
                logger.warning("[Privacy Checker] Фильтрация персональных данных отключена")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки настроек: {e}")
            return False
    
    async def _check_audit_logs(self) -> bool:
        """Проверка логов аудита"""
        try:
            # Проверяем, что есть логи аудита
            if not self.audit_log:
                logger.warning("[Privacy Checker] Нет логов аудита")
                return False
            
            # Проверяем, что не было нарушений приватности
            recent_violations = [
                log for log in self.audit_log[-100:]  # Последние 100 записей
                if not log["success"]
            ]
            
            if len(recent_violations) > 10:  # Более 10 нарушений в последних 100 записях
                logger.warning(f"[Privacy Checker] Обнаружено {len(recent_violations)} нарушений приватности")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки логов аудита: {e}")
            return False
    
    async def _check_gdpr_compliance(self) -> bool:
        """Проверка соответствия GDPR"""
        try:
            # Проверяем, что есть политика конфиденциальности
            # В реальной реализации здесь должна быть проверка наличия политики
            
            # Проверяем, что есть механизм удаления данных
            # В реальной реализации здесь должна быть проверка механизма удаления
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка проверки GDPR: {e}")
            return False
    
    async def get_privacy_report(self) -> Dict[str, Any]:
        """Получение отчета о приватности"""
        try:
            total_checks = len(self.audit_log)
            successful_checks = len([log for log in self.audit_log if log["success"]])
            failed_checks = total_checks - successful_checks
            
            return {
                "privacy_level": self.privacy_level.value,
                "total_checks": total_checks,
                "successful_checks": successful_checks,
                "failed_checks": failed_checks,
                "compliance_rate": (successful_checks / total_checks * 100) if total_checks > 0 else 100,
                "last_check": self.audit_log[-1]["timestamp"] if self.audit_log else None,
                "recent_violations": [
                    log for log in self.audit_log[-10:] if not log["success"]
                ]
            }
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка получения отчета: {e}")
            return {}
    
    async def anonymize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анонимизация данных"""
        try:
            if not settings.DATA_ANONYMIZATION:
                return data
            
            anonymized_data = await self._anonymize_dict(data)
            return anonymized_data
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка анонимизации данных: {e}")
            return data
    
    async def _anonymize_dict(self, data: Any) -> Any:
        """Рекурсивная анонимизация словаря"""
        try:
            if isinstance(data, dict):
                anonymized = {}
                for key, value in data.items():
                    # Анонимизируем ключи
                    anonymized_key = await self._anonymize_key(key)
                    # Анонимизируем значения
                    anonymized_value = await self._anonymize_dict(value)
                    anonymized[anonymized_key] = anonymized_value
                return anonymized
            elif isinstance(data, list):
                return [await self._anonymize_dict(item) for item in data]
            elif isinstance(data, str):
                return await self._anonymize_string(data)
            else:
                return data
                
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка анонимизации словаря: {e}")
            return data
    
    async def _anonymize_key(self, key: str) -> str:
        """Анонимизация ключа"""
        try:
            # Заменяем персональные ключи на общие
            key_mappings = {
                "user_id": "anonymous_id",
                "session_id": "session_token",
                "device_id": "device_token",
                "client_id": "client_token",
                "ip_address": "network_id"
            }
            
            return key_mappings.get(key.lower(), key)
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка анонимизации ключа: {e}")
            return key
    
    async def _anonymize_string(self, text: str) -> str:
        """Анонимизация строки"""
        try:
            # Заменяем email адреса
            text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', text)
            
            # Заменяем IP адреса
            text = re.sub(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '***.***.***.***', text)
            
            # Заменяем номера телефонов
            text = re.sub(r'(\+7|8)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}', '***-***-**-**', text)
            
            return text
            
        except Exception as e:
            logger.error(f"[Privacy Checker] Ошибка анонимизации строки: {e}")
            return text


# Алиас для обратной совместимости
PrivacyChecker = PrivacyComplianceChecker
