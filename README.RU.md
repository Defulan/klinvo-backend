# klinvo-backend

README: [English](README.md) | [Русский](README.RU.md)

Klinvo - минималистичный веб-инструмент для конструирования искусственных языков (конлангов).

* **Документация API:** https://klinvo-backend.onrender.com/docs
* **Технологии:** Python, FastAPI | SQLAlchemy, PostgreSQL, Alembic | Pytest
* **Frontend репозиторий:** [klinvo-frontend ↗](https://github.com/Defulan/klinvo-frontend)

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

## Тестирование
Запустить проверку эндпоинтов:
```bash
task test
```

На данный момент проверки готовы для:
- [x] users.py (/users)
- [x] auth.py (/auth)
- [ ] languages.py (/languages)
- [ ] notes.py (/notes)

## Миграции
Если вы собираетесь сделать миграцию БД
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
│  │  ├─ languages.py - /languages (WIP - в разработке)
│  │  ├─ notes.py - /notes (WIP - в разработке)
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
│  ├─ test_auth.py
│  └─ test_users.py
│
├─ .env.example
├─ .gitignore
├─ alembic.ini
├─ LICENSE
├─ pyproject.toml
├─ pytest.ini
├─ README.md
├─ README.RU.md
└─ requirements.txt
```


## Roadmap
Сейчас основная задача - довести проект до MVP.

### Основные (MVP)
- [x] Система аккаунтов (таблица в БД, создание, вход/выход, изменение, получение данных)
- [ ] Язык (таблица в БД, CRUD)
- [ ] Заметки (таблица в БД, CRUD)
- [ ] Слова (таблица/таблицы в БД, CRUD)

### Дальнейшие
- [ ] Регистрация/Вход по email
- [ ] Блоги сайта (авторская информация о языках/лингвистике)
- [ ] Словообразование (элементы языка, которые позволяют образовывать новые слова из текущих)
- [ ] Транскрипция (отдельный инструмент для удобного описания транскрипции языка)
- [ ] Диалекты языка (несколько колонок для слов, уточнения к значениям)
- [ ] Инструмент описания изменений между языками (фонетические, грамматические и т.д.)

