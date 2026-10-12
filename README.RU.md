# klinvo-backend

README: [English](README.md) | [Русский](README.RU.md)

Klinvo - минималистичный веб-инструмент для конструирования искусственных языков (конлангов).

* **Документация API:** https://klinvo-backend.onrender.com/docs
* **Технологии:** Python, FastAPI | SQLAlchemy, PostgreSQL, Alembic | Pytest | ruff
* **Frontend репозиторий:** [klinvo-frontend ↗](https://github.com/Defulan/klinvo-frontend)
* **[Список изменений](CHANGELOG.md)** *(только на английском)*

> *Примечание: первый запрос может занять 30-60 секунд ожидания из-за холодного старта бесплатного хостинга*

## Как запустить
* **Требования:** Python 3.11+ (писался и тестировался проект на Python 3.13)

1. **Клонировать репозиторий**
```bash
git clone https://github.com/Defulan/klinvo-backend
cd klinvo-backend
```

2. **Создать и активировать виртуальное окружение (venv)**
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Установить библиотеки**
```bash
pip install -r requirements.txt
```

4. **Настроить переменные окружения (.env)**
```bash
cp .env.example .env
```
Переменные в этом проекте такие:
* `SECRET_KEY` - ключ, которым передаются cookie
* `COOKIE_KEY` - значение, которым подписываются значения в cookie
* `FRONTEND_URL` - адрес фронтенда (например: `http://localhost:5173`)
* `DATABASE_URL` - адрес базы данных (например: `postgresql://user:password@localhost:5432/db_name`)
* `TEST_DATABASE_URL` - адрес тестовой базы данных  (например: `postgresql://user:password@localhost:5432/test_db_name`)
* `COOKIE_SECURE` - параметр secure у cookie (`True` если HTTPS, `False` для локальной разработки)
* `COOKIE_SAMESITE` - параметр samesite у cookie (`none` если HTTPS, `lax` для локальной разработки)

5. **Применить миграции базы данных**
```bash
task migrate
```

6. **Запуск сервера**
```bash
task run
```
Если нужно перезагружать после сохранения файла:
```bash
task dev
```
* Интерактивная API документация будет доступна на http://127.0.0.1:8000/docs


## `task` commands
All task commands set up in the `pyproject.toml`.
There is list of all possible commands and below it more specific info:
- `task run` — run the project
- `task dev` — run the project & reload when saving a file
- `task revision "message"` — create alembic migration
- `task migrate` — database migration
- `task test` — run all tests
- `task testusers` — run only `/users` tests
- `task testauth` — run only `/auth` tests
- `task testlang` — run only `/languages` tests
- `task format` — format entire project
- `task format [path]` — format only the specified directory/file
- `task lint` — run linter on the entire project
- `task lint [path]` — run linter only on the specified directory/file
- `task lintdiff` — run linter (`--fix --diff`) on the entire project
- `task lintdiff [path]` — run linter (`--fix --diff`) only on the specified directory/file

### Тестирование
Запустить проверку всех эндпоинтов:
```bash
task test
```
Также вы можете запустить проверку конкретного модуля:
```bash
task testusers
task testauth
task testlang
```

### Форматирование
Запустить форматирование (всего проекта):
```bash
task format
```

Чтобы запустить линтер, нужно ввести одну из команд ниже. `lintdiff` показывает, как именно `task format` сработает. `lint` показывает ошибки без учёта последующих изменений
```bash
task lint
task lintdiff
```

Также можно запустить форматтер только в конкретной папке или файле, например:
```bash
task format app/routers
task lint tests
task lintdiff app/database.py
```

### Миграции
Если вы собираетесь сделать миграцию базы данных:
```bash
task revision "Write here your message"
task migrate
```


## Структура проекта
```
klinvo-backend
├─ .github/ - папка для CI (GitHub Actions)
│
├─ alembic/
│  ├─ versions/ - хранилище миграций
│  ├─ env.py - настройка Alembic
│  └─ script.py.mako
│
├─ app/ - основной код
│  ├─ routers/ - эндпоинты
│  │  ├─ __init__.py
│  │  ├─ auth.py - /auth
│  │  ├─ languages.py - /languages
│  │  ├─ notes.py - /notes
│  │  └─ users.py - /users
│  ├─ __init__.py
│  ├─ config.py - переменная settings с env-значениями
│  ├─ database.py - SQLAlchemy, таблицы, функции для работы с БД
│  ├─ dependencies.py - типы для аргументов эндпоинтов
│  ├─ enums.py
│  ├─ main.py - точка запуска; настройка REST API и подключение эндпоинтов
│  ├─ schemas.py - pydantic схемы
│  └─ security.py - функции для работы с паролями и cookie
│
├─ tests/
│  ├─ conftest.py
│  ├─ enums.py
│  ├─ test_auth.py
│  ├─ test_languages.py
│  ├─ test_notes.py
│  └─ test_users.py
│
├─ .env.example
├─ .gitignore
├─ alembic.ini
├─ LICENSE
├─ pyproject.toml - task-команды и настройка форматтера
├─ pytest.ini
├─ README.md
├─ README.RU.md
└─ requirements.txt
```


## Roadmap
Сейчас основная задача - довести проект до MVP.

### Основные (MVP)
- [x] Система аккаунтов (таблица в БД, создание, вход/выход, изменение, получение данных)
- [x] Языки (таблица в БД, CRUD)
- [x] Заметки (таблица в БД, CRUD)
- [ ] Слова (таблица/таблицы в БД, CRUD)

### Дальнейшие
- [ ] Регистрация/Вход по email
- [ ] Блоги сайта (авторская информация о языках/лингвистике)
- [ ] Словообразование (элементы языка, которые позволяют образовывать новые слова из текущих)
- [ ] Транскрипция (отдельный инструмент для удобного описания транскрипции языка)
- [ ] Диалекты языка (несколько колонок для слов, уточнения к значениям)
- [ ] Инструмент описания изменений между языками (фонетические, грамматические и т.д.)

