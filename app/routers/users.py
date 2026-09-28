from fastapi import APIRouter, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from database import get_db, get_user_by_id, User
from schemas import UserCreateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

hasher = PasswordHash((Argon2Hasher(),))

@router.post("/")
def create_user(data: UserCreateSchema,
                db: Session = Depends(get_db),
                session_id: str | None = Cookie(default=True)):
    if get_user_by_id(session_id) is not None:
        raise HTTPException(status_code=400, detail="User already registered!")
    
    password_hash = hasher.hash(data.password)

    user = User(name=data.name, password_hash=password_hash)
    db.add(user)
    db.commit()

    return {"message": "success"}
