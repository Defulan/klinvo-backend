from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from app.security import hasher, create_cookie, get_value_from_cookie
from app.database import get_user_by_id, User
from app.schemas import UserCreate, UserOut, UserPatch
from app.enums import CookieKey, ErrorCode
from app.dependencies import DbSession, CookieValue

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}")
def get_user(user_id: int, db: DbSession) -> UserOut:
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=400, detail=ErrorCode.USER_DOESNT_EXIST)
    return user


@router.get("/")
def get_users(db: DbSession) -> list[UserOut]:
    return db.scalars(select(User)).all()


@router.post("/")
def create_user(data: UserCreate, response: Response, db: DbSession, session_id: CookieValue = None):
    if session_id:
        raise HTTPException(status_code=400, detail=ErrorCode.AUTHORIZED)
    
    if data.password != data.repassword:
        raise HTTPException(status_code=400, detail=ErrorCode.WRONG_REGISTER_DATA)
    
    password_hash = hasher.hash(data.password)

    user = User(name=data.name, password_hash=password_hash)
    db.add(user)
    db.commit()

    create_cookie(response, CookieKey.SESSION_ID, user.id)

    return {"message": "success"}


@router.patch("/")
def change_user(data: UserPatch, db: DbSession, session_id: CookieValue = None):
    if not session_id:
        raise HTTPException(status_code=403, detail=ErrorCode.UNAUTHORIZED)
    
    user_id = get_value_from_cookie(session_id)
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=400, detail=ErrorCode.USER_DOESNT_EXIST)
    
    filled_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in filled_data.items():
        setattr(user, key, value)
    db.commit()

    return {"message": "success"}
