"""
API модуля Privacy-Compliant Analytics
"""

from .routes import create_api_routes
from .middleware import PrivacyMiddleware, RateLimitMiddleware
from .schemas import *

__all__ = [
    "create_api_routes",
    "PrivacyMiddleware",
    "RateLimitMiddleware"
]
