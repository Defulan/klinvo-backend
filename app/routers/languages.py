from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db, get_user_by_id, Language
from schemas import LanguageCreate, LanguageOut
from security import create_cookie, verify_password, get_value_from_cookie, delete_cookie
from enums import CookieKey, ErrorCode

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
