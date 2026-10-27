from fastapi import APIRouter, status
from sqlalchemy import select
from app.database import Language, get_language_by_id, get_user_by_id
from app.schemas import LanguageCreate, LanguageOut, LanguageEdit, NoteOut, WordOut
from app.security import get_value_from_cookie
from app.dependencies import DbSession, CookieValue
from app.exceptions import (
    NotFoundUserException, UnauthorizedException, NotFoundLanguageException
)

router = APIRouter(
    prefix="/languages",
    tags=["Languages"]
)

@router.get("/")
def get_public_languages(db: DbSession) -> list[LanguageOut]:
    return db.scalars(select(Language).where(Language.is_private == False)).all()


@router.get("/{language_id}")
def get_language(language_id: int, db: DbSession, session_id: CookieValue = None) -> LanguageOut:
    language = get_language_by_id(db, language_id)
    if language is None:
        raise NotFoundLanguageException()
    
    if language.is_private and (not session_id or get_value_from_cookie(session_id) != language.author_id):
        raise NotFoundLanguageException()

    return language


@router.get("/{language_id}/notes")
def get_language_notes(language_id: int, db: DbSession, session_id: CookieValue = None) -> list[NoteOut]:
    language = get_language_by_id(db, language_id)
    if language is None:
        raise NotFoundLanguageException()
    
    if language.is_private and (not session_id or get_value_from_cookie(session_id) != language.author_id):
        raise NotFoundLanguageException()

    return language.notes


@router.get("/{language_id}/words")
def get_language_words(language_id: int, db: DbSession, session_id: CookieValue = None) -> list[WordOut]:
    language = get_language_by_id(db, language_id)
    if language is None:
        raise NotFoundLanguageException()
    
    if language.is_private and (not session_id or int(get_value_from_cookie(session_id)) != language.author_id):
        raise NotFoundLanguageException()

    return language.words


@router.get("/{language_id}/categories")
def get_language_categories(language_id: int, db: DbSession, session_id: CookieValue = None) -> list[WordOut]:
    language = get_language_by_id(db, language_id)
    if language is None:
        raise NotFoundLanguageException()
    
    if language.is_private and (not session_id or int(get_value_from_cookie(session_id)) != language.author_id):
        raise NotFoundLanguageException()

    return language.categories


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_language(data: LanguageCreate, db: DbSession, session_id: CookieValue = None) -> LanguageOut:
    if not session_id:
        raise UnauthorizedException()
    
    author_id = get_value_from_cookie(session_id)
    language = Language(author_id=author_id, name=data.name)
    db.add(language)
    db.commit()
    db.refresh(language)
    
    return language


@router.patch("/{language_id}")
def change_language(language_id: int, data: LanguageEdit, db: DbSession, session_id: CookieValue = None):
    if not session_id:
        raise UnauthorizedException()
    
    language = get_language_by_id(db, language_id)
    if not language:
        raise NotFoundLanguageException()
    
    user_id = get_value_from_cookie(session_id)
    if user_id != language.author_id:
        raise NotFoundLanguageException()
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise NotFoundUserException()
    
    filled_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in filled_data.items():
        setattr(language, key, value)
    db.commit()
    db.refresh(language)
    
    return language
