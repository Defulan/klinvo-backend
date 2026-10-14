from fastapi import APIRouter, HTTPException, status
from app.database import get_user_by_id, get_language_by_id, Note, get_note_by_id
from app.schemas import NoteCreate, NoteOut, NotePatch
from app.security import get_value_from_cookie
from app.enums import ErrorCode
from app.dependencies import DbSession, CookieValue
from app.exceptions import NotFoundUserException, UnauthorizedException, NoPermissionsException, NotFoundLanguageException

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.get("/{note_id}")
def get_note(note_id: int, db: DbSession, session_id: CookieValue = None) -> NoteOut:
    note = get_note_by_id(db, note_id)

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.NOTE_DOESNT_EXIST)
    
    language = note.language
    if language.is_private and (not session_id or get_value_from_cookie(session_id) != language.author_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.NOTE_DOESNT_EXIST)

    return note


@router.post("/{language_id}", status_code=status.HTTP_201_CREATED)
def create_note(language_id: int, data: NoteCreate, db: DbSession, session_id: CookieValue = None) -> NoteOut:
    if not session_id:
        raise UnauthorizedException()
    
    user = get_user_by_id(db, get_value_from_cookie(session_id))
    if not user:
        raise NotFoundUserException()
    
    language = get_language_by_id(db, language_id)
    if not language:
        raise NotFoundLanguageException()
    
    if user.id != language.author_id:
        if language.is_private:
            raise NotFoundLanguageException()
        raise NoPermissionsException()
    
    note = Note(language_id=language_id, title=data.title)
    db.add(note)
    db.commit()

    return note


@router.patch("/{note_id}")
def change_note(note_id: int, data: NotePatch, db: DbSession, session_id: CookieValue = None) -> NoteOut:
    if not session_id:
        raise UnauthorizedException()
    
    note = get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.NOTE_DOESNT_EXIST)
    
    user_id = get_value_from_cookie(session_id)
    if note.language.author_id != user_id:
        if note.language.is_private:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.NOTE_DOESNT_EXIST)
        raise NoPermissionsException()

    filled_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in filled_data.items():
        setattr(note, key, value)
    
    db.commit()
    db.refresh(note)
    
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: DbSession, session_id: CookieValue = None):
    if not session_id:
        raise UnauthorizedException()
    
    note = get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.NOTE_DOESNT_EXIST)
    
    user_id = get_value_from_cookie(session_id)
    if note.language.author_id != user_id:
        if note.language.is_private:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.NOTE_DOESNT_EXIST)
        raise NoPermissionsException()
    
    db.delete(note)
    db.commit()
