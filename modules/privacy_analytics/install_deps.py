#!/usr/bin/env python3
"""
Скрипт установки зависимостей для модуля Privacy Analytics
"""

import sys
import os
from pathlib import Path

# Добавляем путь к модулю
module_dir = Path(__file__).parent
sys.path.insert(0, str(module_dir))

try:
    from dependency_manager import DependencyManager
    
    def main():
        print("🚀 Установка зависимостей модуля Privacy Analytics")
        print("=" * 50)
        
        manager = DependencyManager()
        
        # Проверяем зависимости
        print("🔍 Проверка зависимостей...")
        results = manager.check_all_dependencies(quiet=False)
        
        if "error" in results:
            print(f"❌ {results['error']}")
            return 1
        
        print(f"📊 Статус зависимостей:")
        print(f"   Всего: {results['total']}")
        print(f"   Установлено: {results['installed']}")
        print(f"   Отсутствует: {results['missing']}")
        print(f"   Устарело: {results['outdated']}")
        print()
        
        if results['missing'] > 0 or results['outdated'] > 0:
            print("📦 Установка зависимостей...")
            success = manager.auto_install_dependencies(quiet=False)
            
            if success:
                print("✅ Зависимости успешно установлены!")
                
                # Создаем lock файл
                print("🔒 Создание lock файла...")
                if manager.create_lock_file():
                    print("✅ Lock файл создан")
                else:
                    print("⚠️ Не удалось создать lock файл")
                
                return 0
            else:
                print("❌ Ошибка установки зависимостей")
                return 1
        else:
            print("✅ Все зависимости уже установлены и актуальны!")
            return 0
    
    if __name__ == "__main__":
        exit_code = main()
        sys.exit(exit_code)
        
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что вы запускаете скрипт из правильной директории")
    sys.exit(1)
except Exception as e:
    print(f"❌ Неожиданная ошибка: {e}")
    sys.exit(1)
