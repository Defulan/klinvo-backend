from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db, get_user_by_id, Note
from schemas import NoteCreate, NoteOut
from security import create_cookie, verify_password, get_value_from_cookie, delete_cookie
from enums import CookieKey, ErrorCode

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(Note).where(Note.id == note_id)).first()


@router.get("/{language_id}", response_model=list[NoteOut])
def get_notes(language_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(Note).where(Note.language_id == language_id)).all()
