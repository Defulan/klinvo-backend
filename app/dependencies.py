from typing import Annotated
from fastapi import Depends, Cookie
from sqlalchemy.orm import Session
from database import get_db

DbSession = Annotated[Session, Depends(get_db)]
CookieValue = Annotated[str | None, Cookie()]
