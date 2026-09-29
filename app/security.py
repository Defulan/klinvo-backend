import os
from functools import lru_cache
from fastapi import Response, HTTPException
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from itsdangerous import BadSignature, URLSafeSerializer

hasher = PasswordHash((Argon2Hasher(),))

@lru_cache
def get_serializer():
    return URLSafeSerializer(os.environ.get("COOKIE_KEY"))

def hash_password(password: str) -> str:
    return hasher.hash(password)

def verify_password(entered_password: str, hashed_password: str) -> bool:
    return hasher.verify(entered_password, hashed_password)

def create_cookie(response: Response, key: str, value):
    response.set_cookie(
        key=key,
        value=get_serializer().dumps(value),
        path="/",
        secure=False,
        httponly=True,
        max_age=86400*366,
        samesite="lax"
    )

def get_value_from_cookie(value: str) -> str:
    try:
        return get_serializer().loads(value)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid cookie")
