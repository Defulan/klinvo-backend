import os
from fastapi import APIRouter, Depends, Cookie, HTTPException, Response
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from itsdangerous import BadSignature, URLSafeSerializer
from database import get_db, get_user_by_id, User
from schemas import UserCreateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

hasher = PasswordHash((Argon2Hasher(),))

def get_serializer():
    return URLSafeSerializer(os.environ.get("COOKIE_KEY"))


@router.post("/")
def create_user(data: UserCreateSchema, response: Response,
                db: Session = Depends(get_db),
                session_id: str | None = Cookie(default=True)):
    if get_user_by_id(session_id) is not None:
        raise HTTPException(status_code=400, detail="User already registered!")
    
    password_hash = hasher.hash(data.password)

    user = User(name=data.name, password_hash=password_hash)
    db.add(user)
    db.commit()

    response.set_cookie(
        key="session_id",
        value=get_serializer().dumps(user.id),
        path="/",
        secure=False,
        httponly=True,
        max_age=86400*366,
        samesite="lax"
    )

    return {"message": "success"}
