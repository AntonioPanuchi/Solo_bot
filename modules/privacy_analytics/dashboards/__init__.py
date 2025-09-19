"""
Модуль дашбордов для Privacy-Compliant Analytics
"""

from .realtime_dashboard import RealtimeDashboard
from .admin_dashboard import AdminDashboard
from .business_dashboard import BusinessDashboard

__all__ = [
    "RealtimeDashboard",
    "AdminDashboard", 
    "BusinessDashboard"
]
