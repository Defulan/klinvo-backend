from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db, get_user_by_id, get_language_by_id, Note, Language, get_note_by_id
from app.schemas import NoteCreate, NoteOut, NotePatch
from app.security import get_value_from_cookie
from app.enums import ErrorCode

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteOut:
    return db.scalars(select(Note).where(Note.id == note_id)).first()


@router.get("/{language_id}")
def get_notes(language_id: int, db: Session = Depends(get_db)) -> list[NoteOut]:
    return db.scalars(select(Note).where(Note.language_id == language_id)).all()


@router.post("/")
def create_note(data: NoteCreate, db: Session = Depends(get_db),
                session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED)
    
    language: Language = get_language_by_id(data.language_id)
    if language is None:
        raise HTTPException(status_code=400, detail=ErrorCode.LANGUAGE_DOESNT_EXIST)
    
    session_user_id = get_value_from_cookie(session_id)
    if language.author_id != int(session_user_id):
        raise HTTPException(status_code=403, detail=ErrorCode.NO_PERMISSIONS)

    note = Note(language_id=data.language_id, title=data.title)
    db.add(note)
    db.commit()

    return {"message": "success"}


@router.patch("/")
def change_note(data: NotePatch, db: Session = Depends(get_db),
                session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED)
    
    note: Note = get_note_by_id(db, data.id)
    if note is None:
        raise HTTPException(status_code=400, detail=ErrorCode.NOTE_DOESNT_EXIST)
    
    user = note.language.author
    session_user_id = get_value_from_cookie(session_id)
    if user.id != int(session_user_id):
        raise HTTPException(status_code=403, detail=ErrorCode.NO_PERMISSIONS)
    
    filled_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in filled_data.items():
        setattr(note, key, value)
    db.commit()

    return {"message": "success"}
