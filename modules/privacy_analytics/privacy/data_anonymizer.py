"""
Анонимизация данных для соблюдения приватности
"""

import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import re

from .. import settings
from logger import logger


class DataAnonymizer:
    """Анонимизация данных с соблюдением приватности"""
    
    def __init__(self):
        self.anonymization_rules = self._load_anonymization_rules()
        self.hash_salt = "privacy_analytics_salt_2024"
        
    def _load_anonymization_rules(self) -> Dict[str, Dict[str, Any]]:
        """Загрузка правил анонимизации"""
        return {
            "email": {
                "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "replacement": "user@example.com",
                "method": "replace"
            },
            "phone": {
                "pattern": r'(\+7|8)?[\s\-]?\(?[0-9]{3}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}',
                "replacement": "+7-***-***-**-**",
                "method": "replace"
            },
            "ip_address": {
                "pattern": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                "replacement": "***.***.***.***",
                "method": "replace"
            },
            "user_id": {
                "pattern": r'\buser_id["\']?\s*:\s*["\']?([^"\',\s]+)["\']?',
                "replacement": "user_id: \"anonymous_user\"",
                "method": "replace"
            },
            "session_id": {
                "pattern": r'\bsession_id["\']?\s*:\s*["\']?([^"\',\s]+)["\']?',
                "replacement": "session_id: \"anonymous_session\"",
                "method": "replace"
            },
            "device_id": {
                "pattern": r'\bdevice_id["\']?\s*:\s*["\']?([^"\',\s]+)["\']?',
                "replacement": "device_id: \"anonymous_device\"",
                "method": "replace"
            },
            "credit_card": {
                "pattern": r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                "replacement": "****-****-****-****",
                "method": "replace"
            },
            "passport": {
                "pattern": r'\b\d{4}\s?\d{6}\b',
                "replacement": "**** ******",
                "method": "replace"
            },
            "inn": {
                "pattern": r'\b\d{10,12}\b',
                "replacement": "**********",
                "method": "replace"
            },
            "snils": {
                "pattern": r'\b\d{3}-\d{3}-\d{3}\s\d{2}\b',
                "replacement": "***-***-*** **",
                "method": "replace"
            }
        }
    
    async def anonymize_data(self, data: Union[Dict, List, str, Any]) -> Union[Dict, List, str, Any]:
        """Анонимизация данных"""
        try:
            if not settings.DATA_ANONYMIZATION:
                return data
            
            if isinstance(data, dict):
                return await self._anonymize_dict(data)
            elif isinstance(data, list):
                return await self._anonymize_list(data)
            elif isinstance(data, str):
                return await self._anonymize_string(data)
            else:
                return data
                
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации данных: {e}")
            return data
    
    async def _anonymize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анонимизация словаря"""
        try:
            anonymized = {}
            
            for key, value in data.items():
                # Анонимизируем ключ
                anonymized_key = await self._anonymize_key(key)
                
                # Анонимизируем значение
                if isinstance(value, dict):
                    anonymized_value = await self._anonymize_dict(value)
                elif isinstance(value, list):
                    anonymized_value = await self._anonymize_list(value)
                elif isinstance(value, str):
                    anonymized_value = await self._anonymize_string(value)
                else:
                    anonymized_value = value
                
                anonymized[anonymized_key] = anonymized_value
            
            return anonymized
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации словаря: {e}")
            return data
    
    async def _anonymize_list(self, data: List[Any]) -> List[Any]:
        """Анонимизация списка"""
        try:
            anonymized = []
            
            for item in data:
                if isinstance(item, dict):
                    anonymized_item = await self._anonymize_dict(item)
                elif isinstance(item, list):
                    anonymized_item = await self._anonymize_list(item)
                elif isinstance(item, str):
                    anonymized_item = await self._anonymize_string(item)
                else:
                    anonymized_item = item
                
                anonymized.append(anonymized_item)
            
            return anonymized
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации списка: {e}")
            return data
    
    async def _anonymize_string(self, text: str) -> str:
        """Анонимизация строки"""
        try:
            anonymized_text = text
            
            # Применяем правила анонимизации
            for rule_name, rule in self.anonymization_rules.items():
                if rule["method"] == "replace":
                    anonymized_text = re.sub(
                        rule["pattern"], 
                        rule["replacement"], 
                        anonymized_text, 
                        flags=re.IGNORECASE
                    )
                elif rule["method"] == "hash":
                    anonymized_text = await self._hash_sensitive_data(anonymized_text, rule)
                elif rule["method"] == "mask":
                    anonymized_text = await self._mask_sensitive_data(anonymized_text, rule)
            
            return anonymized_text
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации строки: {e}")
            return text
    
    async def _anonymize_key(self, key: str) -> str:
        """Анонимизация ключа"""
        try:
            # Заменяем персональные ключи на анонимные
            key_mappings = {
                "user_id": "anonymous_id",
                "session_id": "session_token",
                "device_id": "device_token",
                "client_id": "client_token",
                "ip_address": "network_id",
                "email": "contact_info",
                "phone": "contact_info",
                "name": "identifier",
                "surname": "identifier",
                "first_name": "identifier",
                "last_name": "identifier"
            }
            
            return key_mappings.get(key.lower(), key)
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации ключа: {e}")
            return key
    
    async def _hash_sensitive_data(self, text: str, rule: Dict[str, Any]) -> str:
        """Хеширование чувствительных данных"""
        try:
            def hash_replacer(match):
                sensitive_data = match.group(0)
                # Создаем хеш с солью
                hash_object = hashlib.sha256((sensitive_data + self.hash_salt).encode())
                return hash_object.hexdigest()[:8]  # Первые 8 символов хеша
            
            return re.sub(rule["pattern"], hash_replacer, text, flags=re.IGNORECASE)
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка хеширования: {e}")
            return text
    
    async def _mask_sensitive_data(self, text: str, rule: Dict[str, Any]) -> str:
        """Маскирование чувствительных данных"""
        try:
            def mask_replacer(match):
                sensitive_data = match.group(0)
                if len(sensitive_data) <= 4:
                    return "*" * len(sensitive_data)
                else:
                    # Показываем первые 2 и последние 2 символа
                    return sensitive_data[:2] + "*" * (len(sensitive_data) - 4) + sensitive_data[-2:]
            
            return re.sub(rule["pattern"], mask_replacer, text, flags=re.IGNORECASE)
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка маскирования: {e}")
            return text
    
    async def generate_anonymous_id(self, original_id: str) -> str:
        """Генерация анонимного ID"""
        try:
            # Создаем детерминированный анонимный ID
            hash_object = hashlib.sha256((original_id + self.hash_salt).encode())
            return f"anon_{hash_object.hexdigest()[:12]}"
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка генерации анонимного ID: {e}")
            return f"anon_{random.randint(100000, 999999)}"
    
    async def anonymize_timestamp(self, timestamp: Union[str, datetime]) -> str:
        """Анонимизация временной метки"""
        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = timestamp
            
            # Округляем до часа для анонимизации
            anonymized_dt = dt.replace(minute=0, second=0, microsecond=0)
            
            return anonymized_dt.isoformat()
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации временной метки: {e}")
            return timestamp.isoformat() if isinstance(timestamp, datetime) else str(timestamp)
    
    async def anonymize_geographic_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анонимизация географических данных"""
        try:
            anonymized = data.copy()
            
            # Анонимизируем точные координаты
            if "latitude" in anonymized:
                # Округляем до 1 знака после запятой (примерно 11 км точность)
                anonymized["latitude"] = round(float(anonymized["latitude"]), 1)
            
            if "longitude" in anonymized:
                anonymized["longitude"] = round(float(anonymized["longitude"]), 1)
            
            # Анонимизируем IP адреса
            if "ip_address" in anonymized:
                anonymized["ip_address"] = "***.***.***.***"
            
            # Анонимизируем точные адреса
            if "address" in anonymized:
                anonymized["address"] = "***"
            
            return anonymized
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации географических данных: {e}")
            return data
    
    async def anonymize_user_behavior(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анонимизация поведения пользователя"""
        try:
            anonymized = data.copy()
            
            # Анонимизируем конкретные действия
            if "actions" in anonymized and isinstance(anonymized["actions"], list):
                anonymized["actions"] = [
                    await self._anonymize_action(action) 
                    for action in anonymized["actions"]
                ]
            
            # Анонимизируем URL
            if "url" in anonymized:
                anonymized["url"] = await self._anonymize_url(anonymized["url"])
            
            # Анонимизируем пользовательский агент
            if "user_agent" in anonymized:
                anonymized["user_agent"] = "***"
            
            return anonymized
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации поведения пользователя: {e}")
            return data
    
    async def _anonymize_action(self, action: str) -> str:
        """Анонимизация действия пользователя"""
        try:
            # Заменяем конкретные действия на общие категории
            action_mappings = {
                "login": "authentication",
                "logout": "authentication",
                "register": "authentication",
                "view_page": "navigation",
                "click_button": "interaction",
                "submit_form": "interaction",
                "download_file": "resource_access",
                "upload_file": "resource_access"
            }
            
            return action_mappings.get(action.lower(), "user_action")
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации действия: {e}")
            return "user_action"
    
    async def _anonymize_url(self, url: str) -> str:
        """Анонимизация URL"""
        try:
            # Удаляем параметры запроса
            if "?" in url:
                url = url.split("?")[0]
            
            # Заменяем ID в URL на общие значения
            url = re.sub(r'/\d+', '/***', url)
            url = re.sub(r'/[a-f0-9]{8,}', '/***', url)  # UUID и хеши
            
            return url
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка анонимизации URL: {e}")
            return url
    
    async def create_anonymous_dataset(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Создание анонимного набора данных"""
        try:
            anonymous_dataset = []
            
            for item in data:
                anonymized_item = await self.anonymize_data(item)
                anonymous_dataset.append(anonymized_item)
            
            return anonymous_dataset
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка создания анонимного набора данных: {e}")
            return data
    
    async def get_anonymization_report(self, original_data: Any, anonymized_data: Any) -> Dict[str, Any]:
        """Получение отчета об анонимизации"""
        try:
            report = {
                "original_size": len(str(original_data)),
                "anonymized_size": len(str(anonymized_data)),
                "anonymization_rules_applied": len(self.anonymization_rules),
                "data_types_processed": await self._get_processed_data_types(original_data),
                "anonymization_timestamp": datetime.utcnow().isoformat(),
                "privacy_level": settings.PRIVACY_MODE
            }
            
            return report
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка создания отчета: {e}")
            return {}
    
    async def _get_processed_data_types(self, data: Any) -> List[str]:
        """Получение типов обработанных данных"""
        try:
            data_types = set()
            
            if isinstance(data, dict):
                data_types.add("dict")
                for value in data.values():
                    data_types.update(await self._get_processed_data_types(value))
            elif isinstance(data, list):
                data_types.add("list")
                for item in data:
                    data_types.update(await self._get_processed_data_types(item))
            elif isinstance(data, str):
                data_types.add("string")
            elif isinstance(data, (int, float)):
                data_types.add("numeric")
            elif isinstance(data, bool):
                data_types.add("boolean")
            
            return list(data_types)
            
        except Exception as e:
            logger.error(f"[Data Anonymizer] Ошибка получения типов данных: {e}")
            return []
