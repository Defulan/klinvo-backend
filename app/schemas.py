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
    author_id: int
    name: str

class LanguageOut(BaseModel):
    id: int
    author_id: int
    name: str
    created_at: datetime

class NoteCreate(BaseModel):
    language_id: int
    title: str

class NoteOut(BaseModel):
    id: int
    language_id: int
    title: str
    content: str
    created_at: datetime
