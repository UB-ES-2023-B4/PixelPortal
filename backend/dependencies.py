import utils
from schemas import TokenPayload, SystemAccount
from typing import Annotated
from functools import lru_cache
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
import repository
from database import SessionLocal

@lru_cache()
def get_settings():
    return utils.Settings()
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(settings: Annotated[utils.Settings, Depends(get_settings)],
                           token: str = Depends(reuseable_oauth),db: Session = Depends(get_db)) -> SystemAccount:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = token_data.sub

    # get user from database
    user = repository.get_account_by_name(db,username)
    # if user does not exist, raise an exception
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user_dict = user.__dict__

    # Elimina el atributo '_sa_instance_state' si está presente
    user_dict.pop('_sa_instance_state', None)

    # Transforma el diccionario en una instancia de SystemAccount
    system_user = SystemAccount(**user_dict)
    return system_user