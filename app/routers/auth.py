from typing import Annotated
from fastapi import APIRouter, Cookie

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/me")
def get_auth_cookie(session_id: Annotated[str | None, Cookie()] = None):
    is_auth = session_id is not None
    return {"session_id": session_id, "is_auth": is_auth}

