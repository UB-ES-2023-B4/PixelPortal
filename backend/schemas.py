from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    email: str
    contrasena: str
    descripcion: Optional[str] = None
    imagen_perfil_url: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    nombre: str
    email: str
    contrasena: str
    descripcion: str = None
    imagen_perfil_url: Optional[str] = None

class Usuario(UsuarioBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class UsuarioChangePassword(BaseModel):
    current_password: str
    new_password: str
    email: str
class UsuarioChange(BaseModel):
    nombre: str = None
    email: str = None
    descripcion: str = None
    imagen_perfil_url: Optional[str] = None

class UsuarioLogin(UsuarioBase):
    nombre: str = None
    email: str
    contrasena: str
class SeguidorBase(BaseModel):
    seguidor_id: int
    seguido_id: int

class SeguidorCreate(SeguidorBase):
    pass

class Seguidor(SeguidorBase):
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class PublicacionBase(BaseModel):
    usuario_id: int
    usuario_nombre: str
    titulo: str
    descripcion: str
    tags: Optional[str] = None
    imagen_url: Optional[str] = None

class PublicacionCreate(BaseModel):
    titulo: str
    descripcion: str
    usuario_nombre: str
    tags: Optional[str] = None
    imagen_url: Optional[str] = None

class Publicacion(PublicacionBase):
    id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

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
        from_attributes = True

class LikeBase(BaseModel):
    usuario_id: int
    publicacion_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr

class BookMarkBase(BaseModel):
    usuario_id: int
    publicacion_id: int
class BookMarkCreate(BookMarkBase):
    pass
class BookMark(BookMarkBase):
    fecha_creacion: datetime
    class Config:
        from_attributes = True