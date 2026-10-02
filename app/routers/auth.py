from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db, get_user_by_id
from app.schemas import UserLoginSchema
from app.security import create_cookie, verify_password, get_value_from_cookie, delete_cookie
from app.enums import CookieKey, ErrorCode

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/me")
def get_auth_cookie(session_id: Annotated[str | None, Cookie()] = None):
    is_auth = False
    user_id = None
    if session_id is not None:
        is_auth = True
        user_id = get_value_from_cookie(session_id)
    return {"userId": user_id, "isAuth": is_auth}


@router.post("/login")
def login(data: UserLoginSchema, response: Response, db: Session = Depends(get_db),
          session_id: Annotated[str | None, Cookie()] = None):
    if session_id:
        raise HTTPException(status_code=409, detail=ErrorCode.AUTHORIZED)
    
    user = get_user_by_id(db, data.id)
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail=ErrorCode.WRONG_LOGIN_DATA)
    
    create_cookie(response, CookieKey.SESSION_ID, user.id)

    return {"message": "success"}


@router.post("/logout")
def logout(response: Response, db: Session = Depends(get_db),
           session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED)
    
    user_id = get_value_from_cookie(session_id)
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail=ErrorCode.USER_DOESNT_EXIST)
    
    delete_cookie(response, key=CookieKey.SESSION_ID)

    return {"message": "success"}
