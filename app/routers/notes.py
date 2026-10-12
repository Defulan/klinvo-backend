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
