
from passlib.context import CryptContext
from pydantic import BaseSettings
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
import os
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

production= bool(os.getenv("PRODUCTION", False))

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


class Settings(BaseSettings):
    access_token_expire_minutes: int = 30  # 30 minutes
    refresh_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    algorithm: str = "HS256"
    jwt_secret_key: str  # should be kept secret
    jwt_refresh_secret_key: str  # should be kept secret

    class Config:
        env_file = ".env"


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.algorithm)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_refresh_secret_key, settings.algorithm)
    return encoded_jwt


settings = Settings()