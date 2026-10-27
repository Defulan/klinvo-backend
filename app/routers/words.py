from fastapi import APIRouter, status
from app import position
from app.security import get_value_from_cookie
from app.database import get_word_by_id, get_language_by_id, Word, get_user_by_id, get_last_word, get_category_by_id
from app.schemas import WordOut, WordCreate, WordPatch, WordMove
from app.dependencies import DbSession, CookieValue
from app.exceptions import (
    NotFoundWordException, NotFoundLanguageException, NotFoundUserException, NotFoundCategoryException,
    NoPermissionsException, UnauthorizedException
)

router = APIRouter(
    prefix="/words",
    tags=["Words"]
)

@router.get("/{word_id}")
def get_word(word_id: int, db: DbSession, session_id: CookieValue = None) -> WordOut:
    word = get_word_by_id(db, word_id)
    if not word:
        raise NotFoundWordException()
    
    language = get_language_by_id(db, word.language_id)
    if language.is_private and (not session_id or (int(get_value_from_cookie(session_id)) != language.author_id)):
        raise NotFoundWordException()
    
    return word


@router.post("/{language_id}", status_code=status.HTTP_201_CREATED)
def create_word(language_id: int, data: WordCreate, db: DbSession, session_id: CookieValue = None) -> WordOut:
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
    
    last_word: Word = get_last_word(db, language_id, data.category_id)

    if last_word is None:
        new_position = position.get_none_position()
    else:
        new_position = position.new_last_position(last_word.position)

    word = Word(
        language_id=language_id, category_id=data.category_id, position=new_position,
        value=data.value, meaning=data.meaning,
    )

    db.add(word)
    db.commit()

    return word


@router.patch("/{word_id}")
def change_word(word_id: int, data: WordPatch, db: DbSession, session_id: CookieValue) -> WordOut:
    if not session_id:
        raise UnauthorizedException()
    
    user = get_user_by_id(db, get_value_from_cookie(session_id))
    if not user:
        raise NotFoundUserException()
    
    word = get_word_by_id(db, word_id)
    if not word:
        raise NotFoundWordException()

    if user.id != word.language.author_id:
        if word.language.is_private:
            raise NotFoundWordException()
        raise NoPermissionsException()

    filled_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in filled_data.items():
        setattr(word, key, value)
    
    db.commit()
    db.refresh(word)
    
    return word


@router.patch("/{word_id}/move")
def move_word(word_id: int, data: WordMove, db: DbSession, session_id: CookieValue) -> WordOut:
    if not session_id:
        raise UnauthorizedException()
    
    user = get_user_by_id(db, get_value_from_cookie(session_id))
    if not user:
        raise NotFoundUserException()
    
    word = get_word_by_id(db, word_id)
    if not word:
        raise NotFoundWordException()
    
    if word.language.author_id != user.id:
        if word.language.is_private:
            raise NotFoundWordException()
        raise NoPermissionsException()
    
    if data.previous and data.next:
        new_position = position.get_average_position(data.previous, data.next)
    elif data.previous and not data.next:
        new_position = position.new_last_position(data.previous)
    else:
        new_position = position.new_first_position(data.next)
    
    word.position = new_position
    
    db.commit()
    db.refresh(word)

    return word


@router.patch("/{word_id}/move/{category_id}")
def change_word_category(word_id: int, category_id: int, data: WordMove, db: DbSession, session_id: CookieValue) -> WordOut:
    if not session_id:
        raise UnauthorizedException()
    
    user = get_user_by_id(db, get_value_from_cookie(session_id))
    if not user:
        raise NotFoundUserException()
    
    word = get_word_by_id(db, word_id)
    if not word:
        raise NotFoundWordException()
    
    if word.language.author_id != user.id:
        if word.language.is_private:
            raise NotFoundWordException()
        raise NoPermissionsException()
    
    category = get_category_by_id(db, category_id)
    if not category:
        raise NotFoundCategoryException()
    
    word.category_id = category_id
    
    if data.previous and data.next:
        new_position = position.get_average_position(data.previous, data.next)
    elif data.previous and not data.next:
        new_position = position.new_last_position(data.previous)
    else:
        new_position = position.new_first_position(data.next)

    word.position = new_position

    db.commit()
    db.refresh(word)

    return word
