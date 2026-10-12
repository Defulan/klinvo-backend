from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.database import get_user_by_id, get_language_by_id, Note, Language, get_note_by_id
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


@router.post("/{language_id}", status_code=status.HTTP_201_CREATED)
def create_note(language_id: int, data: NoteCreate, db: DbSession, session_id: CookieValue) -> NoteOut:
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ErrorCode.UNAUTHORIZED)
    
    user = get_user_by_id(get_value_from_cookie(session_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.USER_DOESNT_EXIST)
    
    language = get_language_by_id(db, language_id)
    if not language:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.LANGUAGE_DOESNT_EXIST)
    
    if language.is_private and user.id != language.author_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.LANGUAGE_DOESNT_EXIST)
    
    note = Note(language_id=language_id, title=data.title)
    db.add(note)
    db.commit()

    return note
