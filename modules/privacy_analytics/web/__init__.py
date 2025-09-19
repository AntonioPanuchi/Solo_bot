"""
Веб-интерфейс для Privacy-Compliant Analytics
"""

from .app import create_web_app
from .templates import render_template
from .static import serve_static

__all__ = [
    "create_web_app",
    "render_template",
    "serve_static"
]
