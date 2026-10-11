Versions of Backend and Frontend releases at the same time — that is, 
Backend version implies compatible with the corresponding Frontend version


## unreleased

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
- style of README

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
