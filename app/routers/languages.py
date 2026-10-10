from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.database import Language, get_language_by_id, get_user_by_id
from app.schemas import LanguageCreate, LanguageOut, LanguageEdit
from app.security import get_value_from_cookie
from app.enums import ErrorCode
from app.dependencies import DbSession, CookieValue

router = APIRouter(
    prefix="/languages",
    tags=["Languages"]
)

@router.get("/")
def get_languages(db: DbSession) -> list[LanguageOut]:
    return db.scalars(select(Language)).all()


@router.get("/{language_id}")
def get_language(language_id: int, db: DbSession) -> LanguageOut:
    language = get_language_by_id(db, language_id)
    if language is None:
        raise HTTPException(status_code=404, detail=ErrorCode.LANGUAGE_DOESNT_EXIST)
    return language


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_language(data: LanguageCreate, db: DbSession, session_id: CookieValue = None) -> LanguageOut:
    if not session_id:
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED)
    
    author_id = get_value_from_cookie(session_id)
    language = Language(author_id=author_id, name=data.name)
    db.add(language)
    db.commit()
    db.refresh(language)
    
    return language


@router.patch("/{language_id}")
def change_language(language_id: int, data: LanguageEdit, db: DbSession, session_id: CookieValue = None):
    if not session_id:
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED)
    
    language = get_language_by_id(db, language_id)
    if not language:
        raise HTTPException(status_code=404, detail=ErrorCode.LANGUAGE_DOESNT_EXIST)
    
    user_id = get_value_from_cookie(session_id)
    if user_id != language.author_id:
        raise HTTPException(status_code=405, detail=ErrorCode.NO_PERMISSIONS)
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=ErrorCode.USER_DOESNT_EXIST)
    
    filled_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in filled_data.items():
        setattr(language, key, value)
    db.commit()
    db.refresh(language)
    
    return language
