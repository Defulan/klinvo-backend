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
