from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import models, schemas
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import UsuarioCreate
from models import Usuario

from sqlalchemy.orm import Session
from models import Usuario as DBUsuario
from schemas import UsuarioCreate, Usuario

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from dependencies import get_password_hash

def create_user(db: Session, user: schemas.UsuarioCreate):
    hashed_password = get_password_hash(user.contrasena)
    db_user = models.Usuario(
        nombre=user.nombre,
        email=user.email,
        contrasena=hashed_password,  # Guarda la contraseña hasheada
        descripcion=user.descripcion
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




