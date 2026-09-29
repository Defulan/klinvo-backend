import os
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from itsdangerous import BadSignature, URLSafeSerializer

hasher = PasswordHash((Argon2Hasher(),))

def get_serializer():
    return URLSafeSerializer(os.environ.get("COOKIE_KEY"))

def hash_password(password: str) -> str:
    return hasher.hash(password)
