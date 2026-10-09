from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import Language
from app.schemas import LanguageCreate, LanguageOut
from app.security import get_value_from_cookie
from app.enums import ErrorCode
from app.dependencies import DbSession, CookieValue

router = APIRouter(
    prefix="/languages",
    tags=["Languages"]
)

@router.get("/{language_id}")
def get_language(language_id: int, db: DbSession) -> LanguageOut:
    return db.scalars(select(Language).where(Language.id == language_id)).first()


@router.get("/", response_model=list[LanguageOut])
def get_languages(db: DbSession):
    return db.scalars(select(Language)).all()


@router.get("/{user_id}")
def get_user_languages(user_id: int, db: DbSession) -> list[LanguageOut]:
    return db.scalars(select(Language).where(Language.author_id == user_id)).all()


@router.post("/")
def create_language(data: LanguageCreate, db: DbSession, session_id: CookieValue):
    if not session_id:
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED)
    
    author_id = get_value_from_cookie(session_id)
    language = Language(author_id=author_id, name=data.name)
    db.add(language)
    db.commit()

    return {"message": "success"}

