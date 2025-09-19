"""
Автоматическая установка зависимостей для модуля Privacy Analytics
"""

import subprocess
import sys
import os
import importlib
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Современная замена для pkg_resources
try:
    from importlib.metadata import version
    from importlib.metadata import PackageNotFoundError
except ImportError:
    # Fallback для старых версий Python
    try:
        from importlib_metadata import version
        from importlib_metadata import PackageNotFoundError
    except ImportError:
        # Последний fallback - используем pkg_resources
        import pkg_resources
        def version(package_name):
            try:
                return pkg_resources.get_distribution(package_name).version
            except pkg_resources.DistributionNotFound:
                raise PackageNotFoundError(package_name)
        class PackageNotFoundError(Exception):
            pass

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DependencyInstaller:
    """Автоматический установщик зависимостей"""
    
    def __init__(self):
        self.module_dir = Path(__file__).parent
        self.requirements_file = self.module_dir / "requirements.txt"
        self.installed_packages = set()
        self.quiet_mode = True  # Тихий режим для автоматической установки
        
    def check_package_installed(self, package_name: str) -> bool:
        """Проверка установлен ли пакет"""
        try:
            # Убираем версию из названия пакета для проверки
            clean_name = package_name.split('>=')[0].split('==')[0].split('>')[0].split('<')[0]
            importlib.import_module(clean_name)
            return True
        except ImportError:
            return False
    
        def get_package_version(self, package_name: str) -> Optional[str]:
            """Получение версии установленного пакета"""
            try:
                clean_name = package_name.split('>=')[0].split('==')[0].split('>')[0].split('<')[0]
                return version(clean_name)
            except:
                return None
    
    def install_package(self, package: str) -> bool:
        """Установка одного пакета"""
        try:
            if not self.quiet_mode:
                print(f"Установка пакета: {package}")
            
            # Команда установки с тихим режимом
            cmd = [sys.executable, "-m", "pip", "install", package]
            if self.quiet_mode:
                cmd.extend(["--quiet", "--disable-pip-version-check"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if not self.quiet_mode:
                print(f"Пакет {package} успешно установлен")
            return True
            
        except subprocess.CalledProcessError as e:
            if not self.quiet_mode:
                print(f"Ошибка установки пакета {package}: {e}")
                print(f"Вывод: {e.stderr}")
            return False
    
    def install_requirements(self) -> bool:
        """Установка всех зависимостей из requirements.txt"""
        if not self.requirements_file.exists():
            if not self.quiet_mode:
                print("Файл requirements.txt не найден")
            return False
        
        try:
            if not self.quiet_mode:
                print("Установка зависимостей из requirements.txt")
            
            # Команда установки с тихим режимом
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)]
            if self.quiet_mode:
                cmd.extend(["--quiet", "--disable-pip-version-check"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            if not self.quiet_mode:
                print("Все зависимости успешно установлены")
            return True
            
        except subprocess.CalledProcessError as e:
            if not self.quiet_mode:
                print(f"Ошибка установки зависимостей: {e}")
                print(f"Вывод: {e.stderr}")
            return False
    
    def check_and_install_dependencies(self) -> bool:
        """Проверка и установка всех зависимостей"""
        if not self.quiet_mode:
            print("🔍 Проверка зависимостей модуля Privacy Analytics...")
        
        # Список критических зависимостей с минимальными версиями
        critical_deps = [
            "fastapi>=0.104.0",
            "flask>=2.3.0", 
            "pydantic>=2.0.0",
            "sqlalchemy>=2.0.0",
            "psutil>=5.9.0",
            "httpx>=0.25.0",
            "pandas>=2.0.0",
            "numpy>=1.24.0",
            "cryptography>=41.0.0",
            "faker>=19.0.0"
        ]
        
        missing_deps = []
        outdated_deps = []
        
        # Проверяем критические зависимости
        for dep in critical_deps:
            package_name = dep.split('>=')[0]
            required_version = dep.split('>=')[1] if '>=' in dep else None
            
            if not self.check_package_installed(package_name):
                missing_deps.append(dep)
            elif required_version:
                # Проверяем версию
                current_version = self.get_package_version(package_name)
                if current_version and self.compare_versions(current_version, required_version) < 0:
                    outdated_deps.append(dep)
        
        if not missing_deps and not outdated_deps:
            if not self.quiet_mode:
                print("✅ Все критические зависимости установлены и актуальны")
            return True
        
        if missing_deps:
            if not self.quiet_mode:
                print(f"❌ Найдены отсутствующие зависимости: {missing_deps}")
        
        if outdated_deps:
            if not self.quiet_mode:
                print(f"⚠️ Найдены устаревшие зависимости: {outdated_deps}")
        
        # Устанавливаем зависимости
        if self.install_requirements():
            if not self.quiet_mode:
                print("✅ Зависимости успешно установлены")
            return True
        else:
            if not self.quiet_mode:
                print("❌ Не удалось установить зависимости")
            return False
    
    def compare_versions(self, version1: str, version2: str) -> int:
        """Сравнение версий пакетов"""
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Дополняем до одинаковой длины
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            for i in range(max_len):
                if v1_parts[i] < v2_parts[i]:
                    return -1
                elif v1_parts[i] > v2_parts[i]:
                    return 1
            return 0
        except:
            return 0

def auto_install_dependencies(quiet: bool = True) -> bool:
    """Автоматическая установка зависимостей при загрузке модуля"""
    try:
        installer = DependencyInstaller()
        installer.quiet_mode = quiet
        return installer.check_and_install_dependencies()
    except Exception as e:
        if not quiet:
            print(f"❌ Ошибка автоматической установки зависимостей: {e}")
        return False

def manual_install_dependencies() -> bool:
    """Ручная установка зависимостей с подробным выводом"""
    return auto_install_dependencies(quiet=False)

# Автоматическая установка при импорте модуля
if __name__ != "__main__":
    auto_install_dependencies()
else:
    # Запуск вручную
    print("🚀 Установка зависимостей модуля Privacy Analytics")
    success = manual_install_dependencies()
    if success:
        print("🎉 Установка завершена успешно!")
    else:
        print("💥 Установка завершилась с ошибками")
        sys.exit(1)
