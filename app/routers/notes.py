from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.database import get_language_by_id, Note, Language, get_note_by_id
from app.schemas import NoteCreate, NoteOut, NotePatch
from app.security import get_value_from_cookie
from app.enums import ErrorCode
from app.dependencies import DbSession, CookieValue

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.get("/{note_id}")
def get_note(note_id: int, db: DbSession) -> NoteOut:
    return get_note_by_id(db, note_id)
