# klinvo-backend

README: [English](README.md) | [Русский](README.RU.md)

Klinvo is a minimalist web tool for constructing artificial languages (conlangs).

* **API Docs:** https://klinvo-backend.onrender.com/docs
* **Tech stack:** Python, FastAPI | SQLAlchemy, PostgreSQL, Alembic | Pytest
* **Frontend repository:** [klinvo-frontend ↗](https://github.com/Defulan/klinvo-frontend)

* *Note: first request can take 30-60 seconds due to the cold start of free hosting*

## How to Start
* **Requirements:** Python 3.11+ (project was written and tested on Python 3.13)

1. **Clone the repository**
```bash
git clone https://github.com/Defulan/klinvo-backend
cd klinvo-backend
```

2. **Create and activate a virtual environment (venv)**
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

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables (.env)**
```bash
cp .env.example .env
```
.env variables in this project:
* SECRET_KEY - secret key for sessions/cookies
* COOKIE_KEY - key used to sign cookie values
* FRONTEND_URL - frontend URL (e.g., `http://localhost:5173`)
* DATABASE_URL - database connection string (e.g., `postgresql://user:password@localhost:5432/dbname`)
* COOKIE_SECURE - secure param in cookies (`True` if HTTPS, `False` for local development)
* COOKIE_SAMESITE - samesite param in cookies (`none` if HTTPS, `lax` for local development)

5. **Apply database migrations**
```bash
task migrate
```

6. **Run the server**
```bash
task run
```
If you need reloads after saving a file:
```bash
task dev
```
* Interactive API documentation will be available at http://127.0.0.1:8000/docs

## Testing
To run tests of endpoints:
```bash
task test
```

Currently ready tests for:
- [x] users.py (/users)
- [x] auth.py (/auth)
- [ ] languages.py (/languages)
- [ ] notes.py (/notes)


## Migrations
If you want to do database migration:
```bash
task revision "Write here your message"
task migrate
```


## Project structure
```
klinvo-backend
├─ .github/ - directory for CI jobs (GitHub Actions)
│
├─ alembic/
│  ├─ versions/ - migrations storage
│  ├─ env.py - Alembic configuration
│  └─ script.py.mako
│
├─ app/ - main code
│  ├─ routers/ - endpoints
│  │  ├─ __init__.py
│  │  ├─ auth.py - /auth
│  │  ├─ languages.py - /languages (WIP)
│  │  ├─ notes.py - /notes (WIP)
│  │  └─ users.py - /users
│  ├─ __init__.py
│  ├─ config.py - variable settings with environment variables
│  ├─ database.py - SQLAlchemy, tables and database functions
│  ├─ enums.py
│  ├─ main.py - entry point of application
│  ├─ schemas.py - pydantic schemas
│  └─ security.py - functions for password and cookies
│
├─ tests/
│  ├─ conftest.py - fixtures
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
Currently, the main goal is to bring the project to the MVP stage.

### Main (MVP)
- [x] Accounts system (DB table, creating, log in/log out, changing, getting data)
- [x] Database migration (from SQLite to PostgreSQL, add Alembic)
- [ ] Language (DB table, CRUD)
- [ ] Notes (DB table, CRUD)
- [ ] Words (DB table/tables, CRUD)

### Future Enhancements
- [ ] Auth with email
- [ ] Site's blogs (author's information about languages/linguistics)
- [ ] Word formation (language elements which allow to make new words from current)
- [ ] Transcription (instrument for conveniently describing a language's transcription)
- [ ] Dialects (multiple columns for words, clarifications of words meaning)
- [ ] Describing changes in daughter languages
