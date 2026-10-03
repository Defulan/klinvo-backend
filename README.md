# klinvo-backend

README: [English](README.md) | [Русский](README.RU.md)

Klinvo is a web application for constructing artificial languages (conlangs).

* **Tech stack:** Python, FastAPI, SQLAlchemy, SQLite
* **Frontend repository:** [klinvo-frontend](https://github.com/Defulan/klinvo-frontend)

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
* DATABASE_URL - database connection string (e.g., `sqlite:///./data.db`)

5. **Run the server**
```bash
uvicorn app.main:app --reload
```
* Interactive API documentation will be available at http://127.0.0.1:8000/docs


## Project structure (app)
All general code is located in the folder "app"

* `__init__.py`
* `main.py`
* `config.py` - settings for getting .env values
* `database.py` - functions for database; tables and settings for SQLAlchemy
* `security.py` - functions for cookies and passwords
* `enums.py` - enums
* `schemas.py` - pydantic models
* `routers/` - all endpoints
    * `__init__.py`
    * `auth.py` - authentication and getting values from cookies
    * `languages.py` - getting, creating, changing languages
    * `notes.py` - getting, creating, changing notes
    * `users.py` - getting, creating, changing users


## Roadmap
Currently, the main goal is to bring the project to the MVP stage.

### Main (MVP)
- [ ] Accounts system (DB table, creating, log in/log out, changing, getting data)
- [ ] Database migration (SQLite -> PostgreSQL)
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
