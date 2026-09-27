from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.orm import Session
from database import get_db, get_user_by_id
from schemas import UserCreateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/")
def create_user(data: UserCreateSchema,
                db: Session = Depends(get_db),
                session_id: str | None = Cookie(default=True)):
    ...
