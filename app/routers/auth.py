from typing import Annotated
from fastapi import APIRouter, Cookie

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
