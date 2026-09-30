from pydantic import BaseModel
from datetime import datetime

class UserCreateSchema(BaseModel):
    name: str
    password: str
    repassword: str

class UserLoginSchema(BaseModel):
    id: int
    password: str

class UserOut(BaseModel):
    id: int
    name: str

class LanguageCreate(BaseModel):
    name: str

class LanguageOut(BaseModel):
    id: int
    author_id: int
    name: str
    created_at: datetime
    is_private: bool

class NoteCreate(BaseModel):
    language_id: int
    title: str

class NoteOut(BaseModel):
    id: int
    language_id: int
    title: str
    content: str
    created_at: datetime

class NotePatch(BaseModel):
    id: int
    title: str | None
    content: str | None
