from fastapi import APIRouter, Depends, Cookie, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from security import hasher, get_serializer
from database import get_db, get_user_by_id, User
from schemas import UserCreateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=400, detail="User with this ID doesn't exists")    
    return user


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.scalars(select(User)).all()


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
