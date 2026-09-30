from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db, get_user_by_id
from schemas import UserLoginSchema
from security import create_cookie, verify_password, get_value_from_cookie, delete_cookie
from enums import CookieKey, ErrorCode

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)
