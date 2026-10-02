from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db, Language
from app.schemas import LanguageCreate, LanguageOut
from app.security import get_value_from_cookie
from app.enums import ErrorCode

router = APIRouter(
    prefix="/languages",
    tags=["Languages"]
)

@router.get("/{language_id}", response_model=LanguageOut)
def get_language(language_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(Language).where(Language.id == language_id)).first()


@router.get("/", response_model=list[LanguageOut])
def get_languages(db: Session = Depends(get_db)):
    return db.scalars(select(Language)).all()


@router.get("/{user_id}", response_model=list[LanguageOut])
def get_user_languages(user_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(Language).where(Language.author_id == user_id)).all()


@router.post("/")
def create_language(data: LanguageCreate, db: Session = Depends(get_db),
                    session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED)
    
    author_id = get_value_from_cookie(session_id)
    language = Language(author_id=author_id, name=data.name)
    db.add(language)
    db.commit()

    return {"message": "success"}

