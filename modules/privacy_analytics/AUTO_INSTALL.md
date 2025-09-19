# Автоматическая установка зависимостей

## Обзор

Модуль Privacy Analytics теперь поддерживает **полностью автоматическую установку зависимостей** при загрузке. Это означает, что пользователям не нужно вручную устанавливать зависимости - модуль сделает это сам.

## Как это работает

### 1. Автоматическая установка при импорте

Когда модуль импортируется в SoloBot, он автоматически:

1. **Проверяет** все критические зависимости
2. **Сравнивает версии** с требованиями
3. **Устанавливает отсутствующие** пакеты
4. **Обновляет устаревшие** пакеты
5. **Кэширует информацию** о зависимостях

### 2. Компоненты системы

#### `auto_install.py`
- Простая система автоматической установки
- Проверка критических зависимостей
- Тихий режим для автоматической установки

#### `dependency_manager.py`
- Продвинутый менеджер зависимостей
- Поддержка lock файлов
- Кэширование информации
- Детальная проверка версий
- Командная строка

#### `install_deps.py`
- Удобный скрипт для ручной установки
- Подробный вывод процесса
- Создание lock файлов

## Использование

### Автоматическая установка (по умолчанию)

```python
# Просто импортируйте модуль - зависимости установятся автоматически
from modules.privacy_analytics import router, settings
```

### Ручная установка

```bash
# Использование скрипта
python modules/privacy_analytics/install_deps.py

# Через менеджер зависимостей
python -m modules.privacy_analytics.dependency_manager --install --verbose

# Проверка зависимостей
python -m modules.privacy_analytics.dependency_manager --check --verbose
```

## Функции

### ✅ Автоматическая установка
- Проверка при каждом импорте
- Установка отсутствующих пакетов
- Обновление устаревших версий
- Тихий режим (без вывода)

### ✅ Умная проверка версий
- Сравнение версий пакетов
- Поддержка операторов >=, ==, >, <
- Нормализация версий
- Детальная отчетность

### ✅ Кэширование
- Сохранение информации о пакетах
- Быстрая проверка при повторных запусках
- Автоматическое обновление кэша

### ✅ Lock файлы
- Создание requirements.lock
- Установка точных версий
- Воспроизводимые сборки

### ✅ Обработка ошибок
- Graceful fallback при ошибках
- Подробное логирование
- Продолжение работы при сбоях

## Конфигурация

### Переменные окружения

```env
# Отключение автоматической установки
PRIVACY_ANALYTICS_DISABLE_AUTO_INSTALL=true

# Режим отладки
PRIVACY_ANALYTICS_DEBUG_DEPENDENCIES=true

# Путь к pip
PRIVACY_ANALYTICS_PIP_PATH=python -m pip
```

### Настройки в коде

```python
# Отключение автоматической установки
import os
os.environ['PRIVACY_ANALYTICS_DISABLE_AUTO_INSTALL'] = 'true'

# Включение отладочного режима
os.environ['PRIVACY_ANALYTICS_DEBUG_DEPENDENCIES'] = 'true'
```

## Поддерживаемые пакеты

### Критические зависимости
- `fastapi>=0.104.0` - Web framework
- `flask>=2.3.0` - Web framework
- `pydantic>=2.0.0` - Data validation
- `sqlalchemy>=2.0.0` - ORM
- `psutil>=5.9.0` - System monitoring
- `httpx>=0.25.0` - HTTP client
- `pandas>=2.0.0` - Data analysis
- `numpy>=1.24.0` - Numerical computing
- `cryptography>=41.0.0` - Encryption
- `faker>=19.0.0` - Data anonymization

### Дополнительные зависимости
- `python-telegram-bot>=20.0` - Telegram integration
- `redis>=5.0.0` - Caching
- `pytest>=7.4.0` - Testing
- И другие из requirements.txt

## Troubleshooting

### Проблема: Зависимости не устанавливаются

**Решение:**
1. Проверьте права доступа к pip
2. Убедитесь, что pip обновлен
3. Проверьте интернет-соединение
4. Запустите ручную установку

```bash
python modules/privacy_analytics/install_deps.py
```

### Проблема: Конфликты версий

**Решение:**
1. Создайте виртуальное окружение
2. Используйте lock файл
3. Обновите конфликтующие пакеты

```bash
# Создание lock файла
python -m modules.privacy_analytics.dependency_manager --lock

# Установка из lock файла
python -m modules.privacy_analytics.dependency_manager --install-lock
```

### Проблема: Медленная установка

**Решение:**
1. Используйте кэш pip
2. Настройте зеркало PyPI
3. Отключите автоматическую установку

```bash
# Настройка кэша pip
pip config set global.cache-dir ~/.cache/pip

# Отключение автоматической установки
export PRIVACY_ANALYTICS_DISABLE_AUTO_INSTALL=true
```

## Логирование

### Уровни логирования

```python
import logging

# Включение отладочного режима
logging.getLogger('modules.privacy_analytics.dependency_manager').setLevel(logging.DEBUG)
```

### Файлы логов

- `.dependency_cache.json` - Кэш зависимостей
- `requirements.lock` - Lock файл
- Логи pip в стандартном месте

## Безопасность

### Проверка целостности
- Проверка хешей пакетов
- Валидация подписей
- Проверка источников

### Изоляция
- Установка в виртуальное окружение
- Изоляция от системных пакетов
- Контроль версий

## Производительность

### Оптимизации
- Кэширование проверок
- Параллельная установка
- Инкрементальные обновления

### Мониторинг
- Время установки
- Использование памяти
- Сетевой трафик

## Примеры использования

### Базовое использование

```python
# Автоматическая установка при импорте
from modules.privacy_analytics import router, settings

# Модуль готов к использованию
```

### Продвинутое использование

```python
from modules.privacy_analytics.dependency_manager import DependencyManager

# Создание менеджера
manager = DependencyManager()

# Проверка зависимостей
results = manager.check_all_dependencies(quiet=False)
print(f"Установлено: {results['installed']}, Отсутствует: {results['missing']}")

# Установка зависимостей
success = manager.auto_install_dependencies(quiet=False)

# Создание lock файла
manager.create_lock_file()
```

### Командная строка

```bash
# Полная проверка и установка
python modules/privacy_analytics/install_deps.py

# Только проверка
python -m modules.privacy_analytics.dependency_manager --check --verbose

# Создание lock файла
python -m modules.privacy_analytics.dependency_manager --lock

# Очистка кэша
python -m modules.privacy_analytics.dependency_manager --cleanup
```

## Заключение

Автоматическая установка зависимостей делает модуль Privacy Analytics максимально удобным для пользователей. Больше не нужно вручную устанавливать зависимости - модуль сделает это сам при первом запуске.

**Наслаждайтесь простотой использования! 🚀**
