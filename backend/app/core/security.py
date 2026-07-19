from pwdlib import PasswordHash

from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from app.core.config import settings

password_hash= PasswordHash.recommended()

def hash_password(password: str)-> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(data:dict) -> str:
    to_encode=data.copy()

    expire=datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update({"exp":expire})

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

def decode_access_token(token:str):
    try:
        payload=jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except JWTError:
        return None
    