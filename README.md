# klinvo-backend

README: [English](README.md) | [Русский](README.RU.md)

Klinvo is a minimalist web tool for constructing artificial languages (conlangs).

* **API Docs:** https://klinvo-backend.onrender.com/docs
* **Tech stack:** Python, FastAPI | SQLAlchemy, PostgreSQL, Alembic | Pytest | ruff
* **Frontend repository:** [klinvo-frontend ↗](https://github.com/Defulan/klinvo-frontend)
* **[Changelog](CHANGELOG.md)**

> *Note: first request can take 30-60 seconds due to the cold start of free hosting*

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
* `SECRET_KEY` - secret key for sessions/cookies
* `COOKIE_KEY` - key used to sign cookie values
* `FRONTEND_URL` - frontend URL (e.g., `http://localhost:5173`)
* `DATABASE_URL` - database connection string (e.g., `postgresql://user:password@localhost:5432/db_name`)
* `TEST_DATABASE_URL` - test database connection string  (e.g., `postgresql://user:password@localhost:5432/test_db_name`)
* `COOKIE_SECURE` - secure param in cookies (`True` if HTTPS, `False` for local development)
* `COOKIE_SAMESITE` - samesite param in cookies (`none` if HTTPS, `lax` for local development)

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
- `task testnotes` — run only `/notes` tests
- `task format` — format entire project
- `task format [path]` — format only the specified directory/file
- `task lint` — run linter on the entire project
- `task lint [path]` — run linter only on the specified directory/file
- `task lintdiff` — run linter (`--fix --diff`) on the entire project
- `task lintdiff [path]` — run linter (`--fix --diff`) only on the specified directory/file

### Testing
To run tests for all endpoints:
```bash
task test
```
Also you can run tests for specific module:
```bash
task testusers
task testauth
task testlang
task testnotes
```

### Formatting
To run formating (on the entire project):
```bash
task format
```

To run linter, you can write one of these commands below. `lintdiff` shows exactly how `task format` will work. `lint` showing errors without taking subsequent changes into account
```bash
task lint
task lintdiff
```

Also you can run only in the specified directory/file, e.g.:
```bash
task format app/routers
task lint tests
task lintdiff app/database.py
```

### Migrations
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
│  │  ├─ languages.py - /languages
│  │  ├─ notes.py - /notes
│  │  └─ users.py - /users
│  ├─ __init__.py
│  ├─ config.py - variable settings with environment variables
│  ├─ database.py - SQLAlchemy, tables and database functions
│  ├─ dependencies.py - values for endpoints arguments
│  ├─ enums.py
│  ├─ main.py - entry point of application
│  ├─ schemas.py - pydantic schemas
│  └─ security.py - functions for password and cookies
│
├─ tests/
│  ├─ conftest.py - fixtures
│  ├─ enums.py
│  ├─ test_auth.py
│  ├─ test_languages.py
│  ├─ test_notes.py
│  └─ test_users.py
│
├─ .env.example
├─ .gitignore
├─ alembic.ini
├─ CHANGELOG.md
├─ LICENSE
├─ pyproject.toml - task commands and formatter set up
├─ pytest.ini
├─ README.md
├─ README.RU.md
└─ requirements.txt
```


## Roadmap
Currently, the main goal is to bring the project to the MVP stage.

### Main (MVP)
- [x] Accounts system (DB table, creating, log in/log out, changing, getting data)
- [x] Language (DB table, creation, getting, changing)
- [x] Notes (DB table, CRUD)
- [ ] Words (DB table/tables, CRUD)

### Future Enhancements
- [ ] Auth with email
- [ ] Site's blogs (author's information about languages/linguistics)
- [ ] Word formation (language elements which allow to make new words from current)
- [ ] Transcription (instrument for conveniently describing a language's transcription)
- [ ] Dialects (multiple columns for words, clarifications of words meaning)
- [ ] Describing changes in daughter languages
