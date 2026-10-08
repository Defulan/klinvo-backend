# klinvo-backend

README: [English](README.md) | [Русский](README.RU.md)

Klinvo - веб-приложение для конструирования искусственных языков (конлангов).

* **Frontend repository:** [klinvo-frontend ↗](https://github.com/Defulan/klinvo-frontend)
* **API Docs (0.1.1)** https://klinvo-backend.onrender.com/docs
* **Tech stack:** Python, FastAPI | SQLAlchemy, PostgreSQL, Alembic | Pytest
* *Примечание: первый запрос может занять 30-60 секунд ожидания в виду особенностей работs хостинга, где размещён API*

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
* SECRET_KEY - ключ, которым передаются cookie
* COOKIE_KEY - значение, которым подписываются значения в cookie
* FRONTEND_URL - адрес фронтенда (например: `http://localhost:5173`)
* DATABASE_URL - адрес базы данных (например: `postgresql://user:password@localhost:5432/dbname`)
* COOKIE_SECURE - параметр secure у cookie (`True` если HTTPS, `False` для локальной разработки)
* COOKIE_SAMESITE - параметр samesite у cookie (`none` если HTTPS, `lax` для локальной разработки)

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
Весь основной код находится в папке app

* `__init__.py`
* `main.py`
* `config.py` - настройка получения .env файлов
* `database.py` - функции для базы данных; таблицы и настройка SQLAlchemy
* `security.py` - функции для файлов cookie и паролей
* `enums.py` - enums
* `schemas.py` - модели pydantic
* `routers/` - все эндпоинты
    * `__init__.py`
    * `auth.py` - аутентификация и получение данных от cookie
    * `languages.py` - получение, создание и изменение языков
    * `notes.py` - получение, создание и изменение заметок
    * `users.py` - получение, создание и изменение пользователей


## Roadmap
Сейчас основная задача - довести проект до MVP.

### Основные (MVP)
- [x] Система аккаунтов (таблица в БД, создание, вход/выход, изменение, получение данных)
- [x] Миграция базы данных (SQLite -> PostgreSQL, добавление Alembic)
- [ ] Язык (таблица в БД, создание, получение)
- [ ] Заметки (таблица в БД, создание, изменение, получение, удаление)
- [ ] Слова (таблица/таблицы в БД, создание, редактирование, получение, удаление)

### Дальнейшие
- [ ] Регистрация/Вход по email
- [ ] Блоги сайта (авторская информация о языках/лингвистике)
- [ ] Словообразование (элементы языка, которые позволяют образовывать новые слова из текущих)
- [ ] Транскрипция (отдельный инструмент для удобного описания транскрипции языка)
- [ ] Диалекты языка (несколько колонок для слов, уточнения к значениям)
- [ ] Инструмент описания изменений между языками (фонетические, грамматические и т.д.)

