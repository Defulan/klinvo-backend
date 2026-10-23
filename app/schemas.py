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
    title: str = Field(min_length=1, max_length=255)

class NoteOut(ConfiguredBaseModel):
    id: int
    language_id: int
    title: str
    content: str | None
    created_at: datetime

class NotePatch(ConfiguredBaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = Field(default=None)


class WordCreate(ConfiguredBaseModel):
    category_id: int | None = Field(default=None)
    value: str = Field(min_length=1, max_length=255)
    meaning: str = Field(min_length=1, max_length=255)

class WordOut(ConfiguredBaseModel):
    id: int
    language_id: int
    category_id: int | None
    position: str
    value: str
    meaning: str

class WordPatch(ConfiguredBaseModel):
    value: str | None = Field(min_length=1, max_length=255, default=None)
    meaning: str | None = Field(min_length=1, max_length=255, default=None)

class WordMove(ConfiguredBaseModel):
    previous: str | None
    next: str | None

class WordCategoryMove(ConfiguredBaseModel):
    to_bottom: bool = Field(default=False)
    previous: str | None = Field(default=None)
    next: str | None = Field(default=None)

    @model_validator(mode="after")
    def to_bottom_check(self):
        is_previous_filled = self.previous is not None
        is_next_filled = self.next is not None

        if self.to_bottom:
            if is_previous_filled or is_next_filled:
                raise ValueError(ErrorCode.WORD_MOVE_FILLED)
        else:
            if not (is_previous_filled and is_next_filled):
                raise ValueError(ErrorCode.WORD_MOVE_UNFILLED)


class CategoryCreate(ConfiguredBaseModel):
    name: str = Field(min_length=1, max_length=255)

class CategoryOut(ConfiguredBaseModel):
    id: int
    language_id: int
    position: str
    name: str

class CategoryPatch(ConfiguredBaseModel):
    name: str | None = Field(default=None)
