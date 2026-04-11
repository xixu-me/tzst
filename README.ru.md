<h1 align="center">
<img src="https://raw.githubusercontent.com/xixu-me/tzst/refs/heads/main/docs/_static/tzst-logo.png" width="300">
</h1><br>

[![codecov](https://codecov.io/gh/xixu-me/tzst/graph/badge.svg?token=2AIN1559WU)](https://codecov.io/gh/xixu-me/tzst)
[![CodeQL](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/xixu-me/tzst/actions/workflows/ci.yml/badge.svg)](https://github.com/xixu-me/tzst/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/tzst)](https://pypi.org/project/tzst/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/tzst)](https://pypistats.org/packages/tzst)
[![GitHub License](https://img.shields.io/github/license/xixu-me/tzst)](LICENSE)
[![Sponsor](https://img.shields.io/badge/Sponsor-violet)](https://xi-xu.me/#sponsorships)
[![Documentation](https://img.shields.io/badge/Documentation-blue)](https://tzst.xi-xu.me)

[🇺🇸 English](./README.md) | [🇨🇳 汉语](./README.zh.md) | [🇪🇸 español](./README.es.md) | [🇯🇵 日本語](./README.ja.md) | [🇦🇪 العربية](./README.ar.md) | **🇷🇺 русский** | [🇩🇪 Deutsch](./README.de.md) | [🇫🇷 français](./README.fr.md) | [🇰🇷 한국어](./README.ko.md) | [🇧🇷 português](./README.pt.md)

**tzst** — это библиотека и CLI для Python 3.12+, предназначенные для создания, извлечения, просмотра и проверки архивов `.tzst` и `.tar.zst`. Она объединяет совместимость с tar, сжатие Zstandard, потоковый режим, атомарную запись и безопасное извлечение по умолчанию в компактном интерфейсе для production.

> [!NOTE]
> Подробная техническая статья: **[Deep Dive into tzst: A Modern Python Archiving Library Based on Zstandard](https://blog.xi-xu.me/2025/11/01/deep-dive-into-tzst-en.html)**.

## Особенности

- **Высокое сжатие**: Сжатие Zstandard для отличных коэффициентов сжатия и скорости
- **Совместимость с Tar**: Создаёт стандартные tar-архивы, сжатые с помощью Zstandard
- **Интерфейс командной строки**: Интуитивный CLI с поддержкой потоковой передачи и всесторонними опциями
- **Python API**: Чистый, pythonic API для программного использования
- **Кроссплатформенность**: Работает на Windows, macOS и Linux
- **Множественные расширения**: Поддерживает как `.tzst`, так и `.tar.zst` расширения
- **Эффективность памяти**: Режим потоковой передачи для обработки больших архивов с минимальным использованием памяти
- **Атомарные операции**: Безопасные файловые операции с автоматической очисткой при прерывании
- **Безопасность по умолчанию**: Использует фильтр 'data' для максимальной безопасности при извлечении
- **Улучшенная обработка ошибок**: Чёткие сообщения об ошибках с полезными альтернативами

## Установка

### Из релизов GitHub

Скачайте автономные исполняемые файлы, которые не требуют установки Python:

#### Поддерживаемые платформы

| Платформа | Архитектура | Файл |
|----------|-------------|------|
| **Linux** | x86_64 | `tzst-{версия}-linux-amd64.zip` |
| **Linux** | ARM64 | `tzst-{версия}-linux-arm64.zip` |
| **Windows** | x64 | `tzst-{версия}-windows-amd64.zip` |
| **Windows** | ARM64 | `tzst-{версия}-windows-arm64.zip` |
| **macOS** | Intel | `tzst-{версия}-darwin-amd64.zip` |
| **macOS** | Apple Silicon | `tzst-{версия}-darwin-arm64.zip` |

#### Шаги установки

1. **Скачайте** подходящий архив для вашей платформы со [страницы последних релизов](https://github.com/xixu-me/tzst/releases/latest)
2. **Извлеките** архив, чтобы получить исполняемый файл `tzst` (или `tzst.exe` на Windows)
3. **Переместите** исполняемый файл в директорию в вашем PATH:
   - **Linux/macOS**: `sudo mv tzst /usr/local/bin/`
   - **Windows**: Добавьте директорию, содержащую `tzst.exe`, в переменную окружения PATH
4. **Проверьте** установку: `tzst --help`

#### Преимущества бинарной установки

- **Python не требуется** - Автономный исполняемый файл
- **Быстрый запуск** - Нет накладных расходов интерпретатора Python
- **Лёгкое развёртывание** - Распространение одним файлом
- **Последовательное поведение** - Встроенные зависимости

### Из PyPI

Используя pip:

```bash
pip install tzst
```

Или используя uv (рекомендуется):

```bash
uv tool install tzst
```

### Из исходного кода

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install .
```

### Установка для разработки

Этот проект использует современные стандарты упаковки Python:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

## Быстрый старт

### Использование командной строки

```bash
# Создать архив
tzst a archive.tzst file1.txt file2.txt directory/

# Извлечь архив
tzst x archive.tzst

# Список содержимого архива
tzst l archive.tzst

# Проверить целостность архива
tzst t archive.tzst
```

### Использование Python API

```python
from tzst import create_archive, extract_archive, list_archive

# Создать архив
create_archive("archive.tzst", ["file1.txt", "file2.txt", "directory/"])

# Извлечь архив
extract_archive("archive.tzst", "output_directory/")

# Список содержимого архива
contents = list_archive("archive.tzst", verbose=True)
for item in contents:
    print(f"{item['name']}: {item['size']} bytes")
```

## Интерфейс командной строки

### Операции с архивами

#### Создать архив

```bash
# Базовое использование
tzst a archive.tzst file1.txt file2.txt

# С уровнем сжатия (1-22, по умолчанию: 3)
tzst a archive.tzst files/ -l 15

# Альтернативные команды
tzst add archive.tzst files/
tzst create archive.tzst files/
```

#### Извлечь архив

```bash
# Извлечь с полной структурой директорий
tzst x archive.tzst

# Извлечь в определённую директорию
tzst x archive.tzst -o output/

# Извлечь определённые файлы
tzst x archive.tzst file1.txt dir/file2.txt

# Извлечь без структуры директорий (плоско)
tzst e archive.tzst -o output/

# Использовать режим потоковой передачи для больших архивов
tzst x archive.tzst --streaming -o output/
```

#### Список содержимого

```bash
# Простой список
tzst l archive.tzst

# Подробный список с деталями
tzst l archive.tzst -v

# Использовать режим потоковой передачи для больших архивов
tzst l archive.tzst --streaming -v
```

#### Проверка целостности

```bash
# Проверить целостность архива
tzst t archive.tzst

# Проверить с режимом потоковой передачи
tzst t archive.tzst --streaming
```

### Справочник команд

| Команда | Псевдонимы | Описание | Поддержка потоковой передачи |
|---------|---------|-------------|-------------------|
| `a` | `add`, `create` | Создать или добавить в архив | N/A |
| `x` | `extract` | Извлечь с полными путями | ✓ `--streaming` |
| `e` | `extract-flat` | Извлечь без структуры директорий | ✓ `--streaming` |
| `l` | `list` | Список содержимого архива | ✓ `--streaming` |
| `t` | `test` | Проверить целостность архива | ✓ `--streaming` |

### Опции CLI

- `-v, --verbose`: Включить подробный вывод
- `-o, --output DIR`: Указать выходную директорию (команды извлечения)
- `-l, --level LEVEL`: Установить уровень сжатия 1-22 (команда создания)
- `--streaming`: Включить режим потоковой передачи для эффективной обработки памяти
- `--filter FILTER`: Фильтр безопасности для извлечения (data/tar/fully_trusted)
- `--no-atomic`: Отключить атомарные файловые операции (не рекомендуется)

### Фильтры безопасности

```bash
# Извлечь с максимальной безопасностью (по умолчанию)
tzst x archive.tzst --filter data

# Извлечь со стандартной совместимостью tar
tzst x archive.tzst --filter tar

# Извлечь с полным доверием (опасно - только для доверенных архивов)
tzst x archive.tzst --filter fully_trusted
```

**Опции фильтра безопасности:**

- `data` (по умолчанию): Наиболее безопасно. Блокирует опасные файлы, абсолютные пути и пути вне директории извлечения
- `tar`: Стандартная совместимость tar. Блокирует абсолютные пути и обход директорий
- `fully_trusted`: Никаких ограничений безопасности. Используйте только с полностью доверенными архивами

## Python API

### Класс TzstArchive

```python
from tzst import TzstArchive

# Создать новый архив
with TzstArchive("archive.tzst", "w", compression_level=5) as archive:
    archive.add("file.txt")
    archive.add("directory/", recursive=True)

# Прочитать существующий архив
with TzstArchive("archive.tzst", "r") as archive:
    # Список содержимого
    contents = archive.list(verbose=True)
    
    # Извлечь с фильтром безопасности
    archive.extract("file.txt", "output/", filter="data")
    
    # Проверить целостность
    is_valid = archive.test()

# Для больших архивов используйте режим потоковой передачи
with TzstArchive("large_archive.tzst", "r", streaming=True) as archive:
    archive.extract(path="output/")
```

**Важные ограничения:**

- **Режим добавления не поддерживается**: Создавайте множественные архивы или пересоздавайте весь архив вместо этого

### Удобные функции

#### create_archive()

```python
from tzst import create_archive

# Создать с атомарными операциями (по умолчанию)
create_archive(
    archive_path="backup.tzst",
    files=["documents/", "photos/", "config.txt"],
    compression_level=10
)
```

#### extract_archive()

```python
from tzst import extract_archive

# Извлечь с безопасностью (по умолчанию: фильтр 'data')
extract_archive("backup.tzst", "restore/")

# Извлечь определённые файлы
extract_archive("backup.tzst", "restore/", members=["config.txt"])

# Сплющить структуру директорий
extract_archive("backup.tzst", "restore/", flatten=True)

# Использовать потоковую передачу для больших архивов
extract_archive("large_backup.tzst", "restore/", streaming=True)
```

#### list_archive()

```python
from tzst import list_archive

# Простой список
files = list_archive("backup.tzst")

# Подробный список
files = list_archive("backup.tzst", verbose=True)

# Потоковая передача для больших архивов
files = list_archive("large_backup.tzst", streaming=True)
```

#### test_archive()

```python
from tzst import test_archive

# Базовая проверка целостности
if test_archive("backup.tzst"):
    print("Архив действителен")

# Проверка с потоковой передачей
if test_archive("large_backup.tzst", streaming=True):
    print("Большой архив действителен")
```

## Продвинутые возможности

### Расширения файлов

Библиотека автоматически обрабатывает расширения файлов с интеллектуальной нормализацией:

- `.tzst` - Основное расширение для архивов tar+zstandard
- `.tar.zst` - Альтернативное стандартное расширение
- Автоопределение при открытии существующих архивов
- Автоматическое добавление расширения при создании архивов

```python
# Все это создаёт действительные архивы
create_archive("backup.tzst", files)      # Создаёт backup.tzst
create_archive("backup.tar.zst", files)  # Создаёт backup.tar.zst  
create_archive("backup", files)          # Создаёт backup.tzst
create_archive("backup.txt", files)      # Создаёт backup.tzst (нормализовано)
```

### Уровни сжатия

Уровни сжатия Zstandard варьируются от 1 (самый быстрый) до 22 (лучшее сжатие):

- **Уровень 1-3**: Быстрое сжатие, большие файлы
- **Уровень 3** (по умолчанию): Хороший баланс скорости и сжатия
- **Уровень 10-15**: Лучшее сжатие, медленнее
- **Уровень 20-22**: Максимальное сжатие, намного медленнее

### Режим потоковой передачи

Используйте режим потоковой передачи для эффективной обработки больших архивов в памяти:

**Преимущества:**

- Значительно сниженное использование памяти
- Лучшая производительность для архивов, которые не помещаются в память
- Автоматическая очистка ресурсов

**Когда использовать:**

- Архивы больше 100MB
- Среды с ограниченной памятью
- Обработка архивов с множеством больших файлов

```python
# Пример: Обработка большого архива резервной копии
from tzst import extract_archive, list_archive, test_archive

large_archive = "backup_500gb.tzst"

# Операции, эффективные по памяти
is_valid = test_archive(large_archive, streaming=True)
contents = list_archive(large_archive, streaming=True, verbose=True)
extract_archive(large_archive, "restore/", streaming=True)
```

### Атомарные операции

Все операции создания файлов используют атомарные файловые операции по умолчанию:

- Архивы создаются сначала во временных файлах, затем атомарно перемещаются
- Автоматическая очистка при прерывании процесса
- Никакого риска повреждённых или неполных архивов
- Кроссплатформенная совместимость

```python
# Атомарные операции включены по умолчанию
create_archive("important.tzst", files)  # Безопасно от прерывания

# Может быть отключено при необходимости (не рекомендуется)
create_archive("test.tzst", files, use_temp_file=False)
```

### Обработка ошибок

```python
from tzst import TzstArchive
from tzst.exceptions import (
    TzstError,
    TzstArchiveError,
    TzstCompressionError,
    TzstDecompressionError,
    TzstFileNotFoundError
)

try:
    with TzstArchive("archive.tzst", "r") as archive:
        archive.extract()
except TzstDecompressionError:
    print("Не удалось распаковать архив")
except TzstFileNotFoundError:
    print("Файл архива не найден")
except KeyboardInterrupt:
    print("Операция прервана пользователем")
    # Очистка обрабатывается автоматически
```

## Производительность и сравнение

### Советы по производительности

1. **Уровни сжатия**: Уровень 3 оптимален для большинства случаев использования
2. **Потоковая передача**: Используйте для архивов больше 100MB
3. **Пакетные операции**: Добавляйте множественные файлы в одной сессии
4. **Типы файлов**: Уже сжатые файлы не будут сжиматься намного дальше

### против других инструментов

**против tar + gzip:**

- Лучшие коэффициенты сжатия
- Быстрее распаковка
- Современный алгоритм

**против tar + xz:**

- Значительно быстрее сжатие
- Похожие коэффициенты сжатия
- Лучший компромисс скорость/сжатие

**против zip:**

- Лучшее сжатие
- Сохраняет разрешения Unix и метаданные
- Лучшая поддержка потоковой передачи

## Требования

- Python 3.12 или выше
- zstandard >= 0.19.0

## Разработка

### Настройка среды разработки

Этот проект использует современные стандарты упаковки Python:

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
```

### Запуск тестов

```bash
# Запустить тесты с покрытием
pytest --cov=tzst --cov-report=html

# Или использовать более простую команду (настройки покрытия в pyproject.toml)
pytest
```

### Качество кода

```bash
# Проверить качество кода
ruff check src tests

# Форматировать код
ruff format src tests
```

## Вклад

Мы приветствуем вклады! Пожалуйста, прочитайте наше [Руководство по вкладу](CONTRIBUTING.md) для:

- Настройки разработки и структуры проекта
- Руководящих принципов стиля кода и лучших практик
- Требований к тестированию и написанию тестов
- Процесса pull request'ов и рабочего процесса обзора

### Быстрый старт для участников

```bash
git clone https://github.com/xixu-me/tzst.git
cd tzst
pip install -e .[dev]
python -m pytest tests/
```

### Типы приветствуемых вкладов

- **Исправления ошибок** - Исправить проблемы в существующей функциональности
- **Возможности** - Добавить новые возможности в библиотеку
- **Документация** - Улучшить или добавить документацию
- **Тесты** - Добавить или улучшить покрытие тестами
- **Производительность** - Оптимизировать существующий код
- **Безопасность** - Устранить уязвимости безопасности

## Благодарности

- [Meta Zstandard](https://github.com/facebook/zstd) за отличный алгоритм сжатия
- [python-zstandard](https://github.com/indygreg/python-zstandard) за связи Python
- Сообществу Python за вдохновение и обратную связь

## Лицензия

Авторские права &copy; [Си Сюй](https://xi-xu.me). Все права защищены.

Лицензировано под лицензией [BSD 3-Clause](LICENSE).
