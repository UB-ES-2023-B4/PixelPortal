from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import models, schemas
from database import SessionLocal

class UsuarioBase(BaseModel):
    nombre: str
    email: str
    contrasena: str
    descripcion: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    nombre: str
    email: str
    contrasena: str
    descripcion: str = None


class Usuario(UsuarioBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        orm_mode = True

class SeguidorBase(BaseModel):
    seguidor_id: int
    seguido_id: int

class SeguidorCreate(SeguidorBase):
    pass

class Seguidor(SeguidorBase):
    fecha_creacion: datetime
    
    class Config:
        orm_mode = True

class PublicacionBase(BaseModel):
    usuario_id: int
    titulo: str
    descripcion: str
    imagen_url: Optional[str] = None

class PublicacionCreate(PublicacionBase):
    pass

class Publicacion(PublicacionBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        orm_mode = True

class ComentarioBase(BaseModel):
    usuario_id: int
    publicacion_id: int
    contenido: str

class ComentarioCreate(ComentarioBase):
    pass

class Comentario(ComentarioBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        orm_mode = True

class LikeBase(BaseModel):
    usuario_id: int
    publicacion_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    fecha_creacion: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr

