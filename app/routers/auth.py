from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db, get_user_by_id
from schemas import UserLoginSchema
from security import create_cookie, verify_password, get_value_from_cookie, delete_cookie
from enums import CookieKey

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
        raise HTTPException(status_code=409, detail="Client already in account")
    
    user = get_user_by_id(db, data.id)
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Wrong password or ID")
    
    create_cookie(response, CookieKey.SESSION_ID, user.id)

    return {"message": "success"}


@router.post("/logout")
def logout(response: Response, db: Session = Depends(get_db),
           session_id: Annotated[str | None, Cookie()] = None):
    if not session_id:
        raise HTTPException(status_code=401, detail="Client not in account")
    
    user_id = get_value_from_cookie(session_id)
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User doesn't exists")
    
    delete_cookie(response, key=CookieKey.SESSION_ID)

    return {"message": "success"}
