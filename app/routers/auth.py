from fastapi import APIRouter, HTTPException, Response, status
from app.database import get_user_by_id
from app.schemas import UserLogin, AuthOut
from app.security import create_cookie, verify_password, get_value_from_cookie, delete_cookie
from app.enums import CookieKey, ErrorCode
from app.dependencies import DbSession, CookieValue
from app.exceptions import NotFoundUserException, UnauthorizedException, AuthorizedException, WrongLoginException

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/me")
def get_auth_cookie(db: DbSession, session_id: CookieValue = None) -> AuthOut:
    user = None
    if session_id is not None:
        user_id = get_value_from_cookie(session_id)
        user = get_user_by_id(db, user_id)
    
    return AuthOut(user=user)


@router.post("/login")
def login(data: UserLogin, response: Response, db: DbSession, session_id: CookieValue = None):
    if session_id:
        raise AuthorizedException()
    
    user = get_user_by_id(db, data.id)
    if user is None or not verify_password(data.password, user.password_hash):
        raise WrongLoginException()
    
    create_cookie(response, CookieKey.SESSION_ID, user.id)

    return {"message": "success"}


@router.post("/logout")
def logout(response: Response, db: DbSession, session_id: CookieValue = None):
    if not session_id:
        raise UnauthorizedException()
    
    user_id = get_value_from_cookie(session_id)
    user = get_user_by_id(db, user_id)
    if user is None:
        raise NotFoundUserException()
    
    delete_cookie(response, key=CookieKey.SESSION_ID)

    return {"message": "success"}
