"""
Модуль Privacy-Compliant Analytics & Monitoring для SoloBot

Этот модуль предоставляет комплексную систему аналитики и мониторинга
с соблюдением требований приватности пользователей.

Основные возможности:
- Мониторинг серверов и производительности
- Аналитика без нарушения приватности
- Дашборды в реальном времени
- Система алертов и уведомлений
- API для внешних интеграций
- Строгое соблюдение GDPR и других требований
"""

# Автоматическая установка зависимостей при загрузке модуля
try:
    from .dependency_manager import DependencyManager
    dependency_manager = DependencyManager()
    dependency_manager.auto_install_dependencies(quiet=True)
except Exception as e:
    print(f"Предупреждение: Не удалось установить зависимости автоматически: {e}")

from .router import router
from .settings import settings

__version__ = "1.0.0"
__author__ = "SoloBot Team"
__description__ = "Privacy-Compliant Analytics & Monitoring Module"

__all__ = ["router", "settings", "__version__"]
