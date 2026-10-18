from fastapi import APIRouter
from app.security import get_value_from_cookie
from app.database import get_word_by_id, get_language_by_id
from app.schemas import WordOut
from app.dependencies import DbSession, CookieValue
from app.exceptions import NotFoundWordException

router = APIRouter(
    prefix="/words",
    tags=["Words"]
)

@router.get("/{word_id}")
def get_word(word_id: int, db: DbSession, session_id: CookieValue = None) -> WordOut:
    word = get_word_by_id(db, word_id)
    if not word:
        raise NotFoundWordException()
    
    language = get_language_by_id(word.language_id)
    if language.is_private and (not session_id or (int(get_value_from_cookie(session_id)) != language.author_id)):
        raise NotFoundWordException()
    
    return word
