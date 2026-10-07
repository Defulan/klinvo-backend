from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from app.enums import ErrorCode

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    password: str
    repassword: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.repassword:
            raise ValueError(ErrorCode.WRONG_REGISTER_DATA)
        return self

class UserLogin(BaseModel):
    id: int
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    bio: str | None

class UserPatch(BaseModel):
    name: str | None = Field(min_length=1, max_length=50)
    bio: str | None


class LanguageCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)

class LanguageOut(BaseModel):
    id: int
    author_id: int
    name: str
    created_at: datetime
    is_private: bool

class NoteCreate(BaseModel):
    language_id: int
    title: str = Field(min_length=1, max_length=255)

class NoteOut(BaseModel):
    id: int
    language_id: int
    title: str
    content: str
    created_at: datetime

class NotePatch(BaseModel):
    id: int
    title: str | None = Field(min_length=1, max_length=255)
    content: str | None
