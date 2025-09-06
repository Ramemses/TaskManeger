import bcrypt
from datetime import datetime, timedelta
from fastapi import Path
from src.core.config import settings
import jwt




def create_jwt(
        payload: dict,
        private_key: Path=settings.auth_jwt.private_key,
        algorithm: Path=settings.auth_jwt.algorithm,
        expire_minutes: int=settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: int | None = None):

    to_encode = payload.copy()
    expire = None


    now = datetime.now()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    
    to_encode.update({"iat": now})
    to_encode.update({"exp": expire})
    


    encoded = jwt.encode(payload=payload, key=private_key, algorithm=algorithm)



    return encoded



def decode_jwt(
        token: str | bytes,
        public_key: str=settings.auth_jwt.public_key,
        algorithm: str=settings.auth_jwt.algorithm):

    decoded = jwt.decode(token, key=public_key, algorithms=[algorithm])

    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode(), salt=salt)
    return hashed_password


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password=hashed_password)