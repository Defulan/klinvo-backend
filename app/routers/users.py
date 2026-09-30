from typing import Annotated
from fastapi import APIRouter, Depends, Cookie, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from security import hasher, create_cookie, get_value_from_cookie
from database import get_db, get_user_by_id, User
from schemas import UserCreateSchema, UserOut, UserPatch
from enums import CookieKey, ErrorCode

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=400, detail=ErrorCode.USER_DOESNT_EXIST)    
    return user


@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.scalars(select(User)).all()


@router.post("/")
def create_user(data: UserCreateSchema, response: Response,
                db: Session = Depends(get_db),
                session_id: Annotated[str | None, Cookie()] = None):
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
def change_user(data: UserPatch, db: Session = Depends(get_db),
                session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        raise HTTPException(status_code=403, detail=ErrorCode.UNAUTHORIZED)
    
    user_id = get_value_from_cookie(session_id)
    user = get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=400, detail=ErrorCode.USER_DOESNT_EXIST)
    
    filled_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in filled_data.items():
        setattr(user, key, value)
    db.commit()

    return {"message": "success"}
