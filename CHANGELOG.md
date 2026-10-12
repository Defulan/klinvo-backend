Versions of Backend and Frontend releases at the same time — that is, 
Backend version implies compatible with the corresponding Frontend version


## unreleased

#### Added
- ruff formatter
- `task` commands (`format`, `lint`, `lintdiff`)

#### Changed
- Using HTTP codes instead of just numbers
- Returning 201 CREATED code in POST endpoints
- Added section "task commands" in the README (Testing & Migrations are now subsections)


## v0.3.0
#### Added
- /languages endpoints
- /users endpoint for getting languages of specific user
- Tests for all /languages endpoints and for new one in /users
- Specific `task`-commands for tests (`testusers`, `testauth`, `testlang`)
- Implemented Changelog

#### Changed
- CI optimized
- Refactor: argument types of endpoints (`DbSession`, `CookieValue`)
- Disabled `notes.py` module (no more available with fetch/Frontend)

#### Roadmap of this version
- [x] Accounts system (DB table, creating, log in/log out, changing, getting data)
- [x] Language (DB table, creation, getting, changing)
- [ ] Notes (DB table, CRUD)
- [ ] Words (DB table/tables, CRUD)
> In Language CRUD was changed to *creation, getting, changing* because deletion wasn't planned


## 0.2.0
#### Added
- CI jobs for testing and reminding about README updating
- Full Vercel deployment
- Tests for /auth endpoints
- Validation in pydantic schemas
- Task commands (e.g., `task run`, `task test`)

#### Changed
- **❗ /auth/me now returns only `user` and no more `is_auth` & `user_id`**
- Validation errors is more specific
- Style of README

#### Roadmap of this version
- [x] Accounts system (DB table, creating, log in/log out, changing, getting data)
- [ ] Language (DB table, CRUD)
- [ ] Notes (DB table, CRUD)
- [ ] Words (DB table/tables, CRUD)


## 0.1.0
About this first version of the project:
* /auth and /users endpoints
* Testing: only for /users endpoints
* Database: tables User, Language, Note
