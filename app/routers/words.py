from fastapi import APIRouter, status
from app.security import get_value_from_cookie
from app.database import get_word_by_id, get_language_by_id, Word, get_user_by_id, User, Language
from app.schemas import WordOut, WordCreate, WordPatch
from app.dependencies import DbSession, CookieValue
from app.exceptions import NotFoundWordException, NotFoundLanguageException, NotFoundUserException, NoPermissionsException

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


@router.post("/{language_id}", status_code=status.HTTP_201_CREATED)
def create_word(language_id: int, data: WordCreate, db: DbSession, session_id: CookieValue = None) -> WordOut:
    language = get_language_by_id(language_id)
    if not language:
        raise NotFoundLanguageException()
    
    user = get_user_by_id(db, get_value_from_cookie(session_id))
    if not user:
        raise NotFoundUserException()
    
    if not session_id or (user.id != language.author_id):
        if language.is_private:
            raise NotFoundLanguageException()
        raise NoPermissionsException()

    word = Word(language_id=language_id, value=data.value, meaning=data.meaning, category_id=data.category_id)
    db.add(word)
    db.commit()

    return word
