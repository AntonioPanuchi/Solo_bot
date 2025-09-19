"""
Продвинутый менеджер зависимостей для модуля Privacy Analytics
"""

import subprocess
import sys
import os
import importlib
import pkg_resources
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DependencyManager:
    """Продвинутый менеджер зависимостей"""
    
    def __init__(self):
        self.module_dir = Path(__file__).parent
        self.requirements_file = self.module_dir / "requirements.txt"
        self.lock_file = self.module_dir / "requirements.lock"
        self.dependency_cache = self.module_dir / ".dependency_cache.json"
        self.installed_packages = {}
        self.load_cache()
    
    def load_cache(self):
        """Загрузка кэша зависимостей"""
        try:
            if self.dependency_cache.exists():
                with open(self.dependency_cache, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    self.installed_packages = cache_data.get('packages', {})
        except Exception as e:
            logger.warning(f"Не удалось загрузить кэш зависимостей: {e}")
            self.installed_packages = {}
    
    def save_cache(self):
        """Сохранение кэша зависимостей"""
        try:
            cache_data = {
                'packages': self.installed_packages,
                'last_updated': datetime.now().isoformat(),
                'python_version': sys.version
            }
            with open(self.dependency_cache, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Не удалось сохранить кэш зависимостей: {e}")
    
    def get_installed_packages(self) -> Dict[str, str]:
        """Получение списка установленных пакетов"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                check=True
            )
            packages = json.loads(result.stdout)
            return {pkg['name']: pkg['version'] for pkg in packages}
        except Exception as e:
            logger.error(f"Ошибка получения списка пакетов: {e}")
            return {}
    
    def check_dependency(self, package_spec: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Проверка зависимости с версией"""
        try:
            # Парсим спецификацию пакета
            if '>=' in package_spec:
                name, required_version = package_spec.split('>=')
            elif '==' in package_spec:
                name, required_version = package_spec.split('==')
            elif '>' in package_spec:
                name, required_version = package_spec.split('>')
            elif '<' in package_spec:
                name, required_version = package_spec.split('<')
            else:
                name = package_spec
                required_version = None
            
            name = name.strip()
            
            # Проверяем установлен ли пакет
            try:
                importlib.import_module(name)
                installed_version = pkg_resources.get_distribution(name).version
                
                if required_version:
                    # Сравниваем версии
                    if self.compare_versions(installed_version, required_version) >= 0:
                        return True, installed_version, required_version
                    else:
                        return False, installed_version, required_version
                else:
                    return True, installed_version, None
                    
            except ImportError:
                return False, None, required_version
                
        except Exception as e:
            logger.error(f"Ошибка проверки зависимости {package_spec}: {e}")
            return False, None, None
    
    def compare_versions(self, version1: str, version2: str) -> int:
        """Сравнение версий пакетов"""
        try:
            def normalize_version(version):
                return [int(x) for x in version.split('.')]
            
            v1_parts = normalize_version(version1)
            v2_parts = normalize_version(version2)
            
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
    
    def install_dependency(self, package_spec: str, quiet: bool = True) -> bool:
        """Установка одной зависимости"""
        try:
            if not quiet:
                print(f"📦 Установка: {package_spec}")
            
            cmd = [sys.executable, "-m", "pip", "install", package_spec]
            if quiet:
                cmd.extend(["--quiet", "--disable-pip-version-check"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Обновляем кэш
            name = package_spec.split('>=')[0].split('==')[0].split('>')[0].split('<')[0].strip()
            try:
                version = pkg_resources.get_distribution(name).version
                self.installed_packages[name] = version
            except:
                pass
            
            return True
            
        except subprocess.CalledProcessError as e:
            if not quiet:
                print(f"❌ Ошибка установки {package_spec}: {e}")
                print(f"Вывод: {e.stderr}")
            return False
    
    def install_from_requirements(self, quiet: bool = True) -> bool:
        """Установка из requirements.txt"""
        if not self.requirements_file.exists():
            if not quiet:
                print("❌ Файл requirements.txt не найден")
            return False
        
        try:
            if not quiet:
                print("📋 Установка из requirements.txt")
            
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)]
            if quiet:
                cmd.extend(["--quiet", "--disable-pip-version-check"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Обновляем кэш
            self.installed_packages = self.get_installed_packages()
            self.save_cache()
            
            return True
            
        except subprocess.CalledProcessError as e:
            if not quiet:
                print(f"❌ Ошибка установки из requirements.txt: {e}")
                print(f"Вывод: {e.stderr}")
            return False
    
    def check_all_dependencies(self, quiet: bool = True) -> Dict[str, Any]:
        """Проверка всех зависимостей"""
        if not self.requirements_file.exists():
            return {"error": "Файл requirements.txt не найден"}
        
        try:
            with open(self.requirements_file, 'r', encoding='utf-8') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            results = {
                "total": len(requirements),
                "installed": 0,
                "missing": 0,
                "outdated": 0,
                "packages": {}
            }
            
            for req in requirements:
                is_installed, installed_ver, required_ver = self.check_dependency(req)
                
                package_name = req.split('>=')[0].split('==')[0].split('>')[0].split('<')[0].strip()
                
                if is_installed:
                    results["installed"] += 1
                    status = "installed"
                    if required_ver and installed_ver != required_ver:
                        status = "outdated"
                        results["outdated"] += 1
                else:
                    results["missing"] += 1
                    status = "missing"
                
                results["packages"][package_name] = {
                    "specification": req,
                    "status": status,
                    "installed_version": installed_ver,
                    "required_version": required_ver
                }
            
            return results
            
        except Exception as e:
            return {"error": f"Ошибка проверки зависимостей: {e}"}
    
    def auto_install_dependencies(self, quiet: bool = True) -> bool:
        """Автоматическая установка всех зависимостей"""
        try:
            if not quiet:
                print("🔍 Проверка зависимостей модуля Privacy Analytics...")
            
            # Проверяем зависимости
            check_results = self.check_all_dependencies(quiet)
            
            if "error" in check_results:
                if not quiet:
                    print(f"❌ {check_results['error']}")
                return False
            
            if check_results["missing"] == 0 and check_results["outdated"] == 0:
                if not quiet:
                    print("✅ Все зависимости установлены и актуальны")
                return True
            
            if not quiet:
                print(f"📊 Найдено: {check_results['missing']} отсутствующих, {check_results['outdated']} устаревших")
            
            # Устанавливаем зависимости
            if self.install_from_requirements(quiet):
                if not quiet:
                    print("✅ Зависимости успешно установлены")
                return True
            else:
                if not quiet:
                    print("❌ Не удалось установить зависимости")
                return False
                
        except Exception as e:
            if not quiet:
                print(f"❌ Ошибка автоматической установки: {e}")
            return False
    
    def create_lock_file(self) -> bool:
        """Создание lock файла с точными версиями"""
        try:
            installed = self.get_installed_packages()
            
            with open(self.lock_file, 'w', encoding='utf-8') as f:
                f.write("# Lock file for Privacy Analytics module\n")
                f.write(f"# Generated: {datetime.now().isoformat()}\n")
                f.write(f"# Python: {sys.version}\n\n")
                
                for name, version in sorted(installed.items()):
                    f.write(f"{name}=={version}\n")
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка создания lock файла: {e}")
            return False
    
    def install_from_lock_file(self, quiet: bool = True) -> bool:
        """Установка из lock файла"""
        if not self.lock_file.exists():
            if not quiet:
                print("❌ Lock файл не найден")
            return False
        
        try:
            if not quiet:
                print("🔒 Установка из lock файла")
            
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(self.lock_file)]
            if quiet:
                cmd.extend(["--quiet", "--disable-pip-version-check"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return True
            
        except subprocess.CalledProcessError as e:
            if not quiet:
                print(f"❌ Ошибка установки из lock файла: {e}")
            return False
    
    def cleanup_cache(self):
        """Очистка кэша зависимостей"""
        try:
            if self.dependency_cache.exists():
                self.dependency_cache.unlink()
            if self.lock_file.exists():
                self.lock_file.unlink()
            print("🧹 Кэш зависимостей очищен")
        except Exception as e:
            print(f"❌ Ошибка очистки кэша: {e}")

def main():
    """Главная функция для командной строки"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Менеджер зависимостей Privacy Analytics")
    parser.add_argument("--check", action="store_true", help="Проверить зависимости")
    parser.add_argument("--install", action="store_true", help="Установить зависимости")
    parser.add_argument("--lock", action="store_true", help="Создать lock файл")
    parser.add_argument("--install-lock", action="store_true", help="Установить из lock файла")
    parser.add_argument("--cleanup", action="store_true", help="Очистить кэш")
    parser.add_argument("--verbose", "-v", action="store_true", help="Подробный вывод")
    
    args = parser.parse_args()
    
    manager = DependencyManager()
    quiet = not args.verbose
    
    if args.check:
        results = manager.check_all_dependencies(quiet)
        if "error" in results:
            print(f"❌ {results['error']}")
        else:
            print(f"📊 Всего: {results['total']}, Установлено: {results['installed']}, Отсутствует: {results['missing']}, Устарело: {results['outdated']}")
    
    elif args.install:
        success = manager.auto_install_dependencies(quiet)
        sys.exit(0 if success else 1)
    
    elif args.lock:
        success = manager.create_lock_file()
        print("✅ Lock файл создан" if success else "❌ Ошибка создания lock файла")
    
    elif args.install_lock:
        success = manager.install_from_lock_file(quiet)
        sys.exit(0 if success else 1)
    
    elif args.cleanup:
        manager.cleanup_cache()
    
    else:
        # По умолчанию - автоматическая установка
        success = manager.auto_install_dependencies(quiet)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
