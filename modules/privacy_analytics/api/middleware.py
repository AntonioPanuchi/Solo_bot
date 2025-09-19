"""
Middleware для API Privacy-Compliant Analytics
"""

import time
import asyncio
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
import hashlib
import hmac

from .. import settings
from ..privacy import PrivacyComplianceChecker
from logger import logger


class PrivacyMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки соответствия требованиям приватности"""
    
    def __init__(self, app):
        super().__init__(app)
        self.privacy_checker = PrivacyComplianceChecker()
        
    async def dispatch(self, request: Request, call_next):
        """Обработка запроса с проверкой приватности"""
        try:
            # Проверяем соответствие требованиям приватности
            if not await self.check_privacy_compliance(request):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "Privacy compliance violation",
                        "message": "Запрос не соответствует требованиям приватности",
                        "timestamp": time.time()
                    }
                )
            
            # Обрабатываем запрос
            response = await call_next(request)
            
            # Проверяем ответ на соответствие требованиям приватности
            if not await self.check_response_privacy(response):
                logger.warning(f"[Privacy Middleware] Ответ не прошел проверку приватности: {request.url}")
            
            return response
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка обработки запроса: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "message": "Ошибка обработки запроса",
                    "timestamp": time.time()
                }
            )
    
    async def check_privacy_compliance(self, request: Request) -> bool:
        """Проверка соответствия запроса требованиям приватности"""
        try:
            # Проверяем заголовки запроса
            if not await self.check_request_headers(request):
                return False
            
            # Проверяем параметры запроса
            if not await self.check_request_parameters(request):
                return False
            
            # Проверяем тело запроса (если есть)
            if request.method in ["POST", "PUT", "PATCH"]:
                if not await self.check_request_body(request):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка проверки приватности: {e}")
            return False
    
    async def check_request_headers(self, request: Request) -> bool:
        """Проверка заголовков запроса"""
        try:
            # Проверяем наличие обязательных заголовков
            required_headers = ["User-Agent", "Accept"]
            for header in required_headers:
                if header not in request.headers:
                    logger.warning(f"[Privacy Middleware] Отсутствует обязательный заголовок: {header}")
                    return False
            
            # Проверяем запрещенные заголовки
            forbidden_headers = ["X-Forwarded-For", "X-Real-IP"]
            for header in forbidden_headers:
                if header in request.headers:
                    logger.warning(f"[Privacy Middleware] Обнаружен запрещенный заголовок: {header}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка проверки заголовков: {e}")
            return False
    
    async def check_request_parameters(self, request: Request) -> bool:
        """Проверка параметров запроса"""
        try:
            # Проверяем параметры на наличие персональных данных
            query_params = dict(request.query_params)
            
            for param, value in query_params.items():
                if await self.contains_personal_data(param, value):
                    logger.warning(f"[Privacy Middleware] Параметр содержит персональные данные: {param}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка проверки параметров: {e}")
            return False
    
    async def check_request_body(self, request: Request) -> bool:
        """Проверка тела запроса"""
        try:
            # Читаем тело запроса
            body = await request.body()
            
            if body:
                # Проверяем на наличие персональных данных
                if await self.contains_personal_data("body", body.decode()):
                    logger.warning("[Privacy Middleware] Тело запроса содержит персональные данные")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка проверки тела запроса: {e}")
            return False
    
    async def check_response_privacy(self, response) -> bool:
        """Проверка ответа на соответствие требованиям приватности"""
        try:
            # Проверяем заголовки ответа
            if not await self.check_response_headers(response):
                return False
            
            # Проверяем содержимое ответа
            if not await self.check_response_content(response):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка проверки ответа: {e}")
            return False
    
    async def check_response_headers(self, response) -> bool:
        """Проверка заголовков ответа"""
        try:
            # Проверяем наличие заголовков приватности
            privacy_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options",
                "X-XSS-Protection"
            ]
            
            for header in privacy_headers:
                if header not in response.headers:
                    logger.warning(f"[Privacy Middleware] Отсутствует заголовок безопасности: {header}")
            
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка проверки заголовков ответа: {e}")
            return False
    
    async def check_response_content(self, response) -> bool:
        """Проверка содержимого ответа"""
        try:
            # Здесь должна быть логика проверки содержимого ответа
            # на соответствие требованиям приватности
            return True
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка проверки содержимого ответа: {e}")
            return False
    
    async def contains_personal_data(self, field: str, value: Any) -> bool:
        """Проверка на наличие персональных данных"""
        try:
            if not isinstance(value, str):
                return False
            
            # Проверяем запрещенные паттерны
            forbidden_patterns = settings.FORBIDDEN_DATA_PATTERNS
            
            for pattern in forbidden_patterns:
                if pattern.lower() in field.lower() or pattern.lower() in value.lower():
                    return True
            
            # Проверяем на email адреса
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.search(email_pattern, value):
                return True
            
            # Проверяем на IP адреса
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            if re.search(ip_pattern, value):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"[Privacy Middleware] Ошибка проверки персональных данных: {e}")
            return False


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для ограничения скорости запросов"""
    
    def __init__(self, app):
        super().__init__(app)
        self.rate_limits = defaultdict(lambda: deque(maxlen=1000))
        self.rate_limit = settings.API_RATE_LIMIT  # запросов в час
        
    async def dispatch(self, request: Request, call_next):
        """Обработка запроса с проверкой лимитов"""
        try:
            # Получаем идентификатор клиента
            client_id = await self.get_client_id(request)
            
            # Проверяем лимит запросов
            if not await self.check_rate_limit(client_id):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "Rate limit exceeded",
                        "message": f"Превышен лимит запросов: {self.rate_limit} в час",
                        "retry_after": 3600,
                        "timestamp": time.time()
                    }
                )
            
            # Записываем запрос
            await self.record_request(client_id)
            
            # Обрабатываем запрос
            response = await call_next(request)
            
            return response
            
        except Exception as e:
            logger.error(f"[Rate Limit Middleware] Ошибка обработки запроса: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "message": "Ошибка обработки запроса",
                    "timestamp": time.time()
                }
            )
    
    async def get_client_id(self, request: Request) -> str:
        """Получение идентификатора клиента"""
        try:
            # Пытаемся получить IP адрес
            client_ip = request.client.host
            
            # Проверяем заголовки прокси
            forwarded_for = request.headers.get("X-Forwarded-For")
            if forwarded_for:
                client_ip = forwarded_for.split(",")[0].strip()
            
            real_ip = request.headers.get("X-Real-IP")
            if real_ip:
                client_ip = real_ip
            
            # Создаем хэш для анонимизации
            client_hash = hashlib.sha256(client_ip.encode()).hexdigest()[:16]
            
            return client_hash
            
        except Exception as e:
            logger.error(f"[Rate Limit Middleware] Ошибка получения ID клиента: {e}")
            return "unknown"
    
    async def check_rate_limit(self, client_id: str) -> bool:
        """Проверка лимита запросов"""
        try:
            current_time = time.time()
            hour_ago = current_time - 3600  # 1 час назад
            
            # Получаем запросы за последний час
            requests = self.rate_limits[client_id]
            
            # Удаляем старые запросы
            while requests and requests[0] < hour_ago:
                requests.popleft()
            
            # Проверяем лимит
            if len(requests) >= self.rate_limit:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Rate Limit Middleware] Ошибка проверки лимита: {e}")
            return True  # В случае ошибки разрешаем запрос
    
    async def record_request(self, client_id: str):
        """Запись запроса"""
        try:
            current_time = time.time()
            self.rate_limits[client_id].append(current_time)
            
        except Exception as e:
            logger.error(f"[Rate Limit Middleware] Ошибка записи запроса: {e}")
    
    async def get_rate_limit_status(self, client_id: str) -> Dict[str, Any]:
        """Получение статуса лимита для клиента"""
        try:
            current_time = time.time()
            hour_ago = current_time - 3600
            
            # Получаем запросы за последний час
            requests = self.rate_limits[client_id]
            
            # Удаляем старые запросы
            while requests and requests[0] < hour_ago:
                requests.popleft()
            
            return {
                "client_id": client_id,
                "requests_count": len(requests),
                "rate_limit": self.rate_limit,
                "remaining": max(0, self.rate_limit - len(requests)),
                "reset_time": current_time + 3600
            }
            
        except Exception as e:
            logger.error(f"[Rate Limit Middleware] Ошибка получения статуса лимита: {e}")
            return {}


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware для безопасности"""
    
    def __init__(self, app):
        super().__init__(app)
        self.blocked_ips = set()
        self.suspicious_requests = defaultdict(int)
        
    async def dispatch(self, request: Request, call_next):
        """Обработка запроса с проверкой безопасности"""
        try:
            # Проверяем IP адрес
            if not await self.check_ip_address(request):
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "error": "Access denied",
                        "message": "IP адрес заблокирован",
                        "timestamp": time.time()
                    }
                )
            
            # Проверяем подозрительную активность
            if not await self.check_suspicious_activity(request):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "Suspicious activity detected",
                        "message": "Обнаружена подозрительная активность",
                        "timestamp": time.time()
                    }
                )
            
            # Обрабатываем запрос
            response = await call_next(request)
            
            # Добавляем заголовки безопасности
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            
            return response
            
        except Exception as e:
            logger.error(f"[Security Middleware] Ошибка обработки запроса: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "message": "Ошибка обработки запроса",
                    "timestamp": time.time()
                }
            )
    
    async def check_ip_address(self, request: Request) -> bool:
        """Проверка IP адреса"""
        try:
            # Получаем IP адрес
            client_ip = request.client.host
            
            # Проверяем, не заблокирован ли IP
            if client_ip in self.blocked_ips:
                return False
            
            # Здесь должна быть логика проверки IP через черные списки
            # Для примера просто возвращаем True
            return True
            
        except Exception as e:
            logger.error(f"[Security Middleware] Ошибка проверки IP: {e}")
            return True
    
    async def check_suspicious_activity(self, request: Request) -> bool:
        """Проверка подозрительной активности"""
        try:
            # Получаем идентификатор клиента
            client_id = await self.get_client_id(request)
            
            # Увеличиваем счетчик запросов
            self.suspicious_requests[client_id] += 1
            
            # Проверяем лимит подозрительных запросов
            if self.suspicious_requests[client_id] > 100:  # 100 запросов в час
                logger.warning(f"[Security Middleware] Подозрительная активность: {client_id}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"[Security Middleware] Ошибка проверки подозрительной активности: {e}")
            return True
    
    async def get_client_id(self, request: Request) -> str:
        """Получение идентификатора клиента"""
        try:
            client_ip = request.client.host
            user_agent = request.headers.get("User-Agent", "")
            
            # Создаем хэш для идентификации клиента
            client_string = f"{client_ip}:{user_agent}"
            client_hash = hashlib.sha256(client_string.encode()).hexdigest()[:16]
            
            return client_hash
            
        except Exception as e:
            logger.error(f"[Security Middleware] Ошибка получения ID клиента: {e}")
            return "unknown"
    
    async def block_ip(self, ip: str):
        """Блокировка IP адреса"""
        try:
            self.blocked_ips.add(ip)
            logger.info(f"[Security Middleware] IP заблокирован: {ip}")
            
        except Exception as e:
            logger.error(f"[Security Middleware] Ошибка блокировки IP: {e}")
    
    async def unblock_ip(self, ip: str):
        """Разблокировка IP адреса"""
        try:
            self.blocked_ips.discard(ip)
            logger.info(f"[Security Middleware] IP разблокирован: {ip}")
            
        except Exception as e:
            logger.error(f"[Security Middleware] Ошибка разблокировки IP: {e}")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирования запросов"""
    
    def __init__(self, app):
        super().__init__(app)
        
    async def dispatch(self, request: Request, call_next):
        """Обработка запроса с логированием"""
        try:
            # Логируем начало запроса
            start_time = time.time()
            
            logger.info(f"[API Request] {request.method} {request.url} - {request.client.host}")
            
            # Обрабатываем запрос
            response = await call_next(request)
            
            # Логируем завершение запроса
            end_time = time.time()
            duration = end_time - start_time
            
            logger.info(f"[API Response] {request.method} {request.url} - {response.status_code} - {duration:.3f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"[Logging Middleware] Ошибка обработки запроса: {e}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal server error",
                    "message": "Ошибка обработки запроса",
                    "timestamp": time.time()
                }
            )
