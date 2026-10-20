from fastapi import APIRouter, status
from app.security import get_value_from_cookie
from app.database import get_category_by_id, get_language_by_id, Category, get_user_by_id, get_last_category
from app.schemas import CategoryOut, CategoryCreate, CategoryPatch
from app.position import Position
from app.dependencies import DbSession, CookieValue
from app.exceptions import (
    NotFoundCategoryException, NotFoundLanguageException, NotFoundUserException,
    NoPermissionsException, UnauthorizedException
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/{category_id}")
def get_category(category_id: int, db: DbSession, session_id: CookieValue = None) -> CategoryOut:
    category = get_category_by_id(db, category_id)
    if not category:
        raise NotFoundCategoryException()
    
    language = get_language_by_id(db, category.language_id)
    if language.is_private and (not session_id or (int(get_value_from_cookie(session_id)) != language.author_id)):
        raise NotFoundCategoryException()
    
    return category


@router.post("/{language_id}", status_code=status.HTTP_201_CREATED)
def create_category(language_id: int, data: CategoryCreate, db: DbSession, session_id: CookieValue = None) -> CategoryOut:
    language = get_language_by_id(db, language_id)
    if not language:
        raise NotFoundLanguageException()
    
    user = get_user_by_id(db, get_value_from_cookie(session_id))
    if not user:
        raise NotFoundUserException()
    
    if not session_id or (user.id != language.author_id):
        if language.is_private:
            raise NotFoundLanguageException()
        raise NoPermissionsException()
    
    last_category: Category = get_last_category(db, language_id)

    if last_category is None:
        new_position = Position.none_position_value()
    else:
        new_position = Position(last_category.position).get_next_position_value()

    category = Category(
        language_id=language_id, position=new_position,
        name=data.name
    )

    db.add(category)
    db.commit()

    return category


@router.patch("/{category_id}")
def change_category(category_id: int, data: CategoryPatch, db: DbSession, session_id: CookieValue) -> CategoryOut:
    if not session_id:
        raise UnauthorizedException()
    
    category = get_category_by_id(db, category_id)
    if not category:
        raise NotFoundCategoryException()
    
    user = get_user_by_id(db, get_value_from_cookie(session_id))
    if not user:
        raise NotFoundUserException()

    if user.id != category.language.author_id:
        if category.language.is_private:
            raise NotFoundCategoryException()
        raise NoPermissionsException()

    filled_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in filled_data.items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    
    return category
