from pydantic import BaseModel, Field, model_validator
from pydantic.alias_generators import to_camel
from datetime import datetime
from app.enums import ErrorCode

class ConfiguredBaseModel(BaseModel):
    model_config = {
        "from_attributes": True,
        "alias_generator": to_camel,
        "populate_by_name": True
    }

class UserCreate(ConfiguredBaseModel):
    name: str = Field(min_length=1, max_length=50)
    password: str
    repassword: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.repassword:
            raise ValueError(ErrorCode.WRONG_REGISTER_DATA)
        return self

class UserLogin(ConfiguredBaseModel):
    id: int
    password: str

class UserOut(ConfiguredBaseModel):
    id: int
    name: str
    bio: str | None

class UserPatch(ConfiguredBaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    bio: str | None = None


class AuthOut(ConfiguredBaseModel):
    user: UserOut | None


class LanguageCreate(ConfiguredBaseModel):
    name: str = Field(min_length=1, max_length=255)

class LanguageOut(ConfiguredBaseModel):
    id: int
    author_id: int
    name: str
    created_at: datetime
    is_private: bool

class LanguageEdit(ConfiguredBaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    is_private: bool | None = Field(default=None)


class NoteCreate(ConfiguredBaseModel):
    language_id: int
    title: str = Field(min_length=1, max_length=255)

class NoteOut(ConfiguredBaseModel):
    id: int
    language_id: int
    title: str
    content: str
    created_at: datetime

class NotePatch(ConfiguredBaseModel):
    id: int
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None
