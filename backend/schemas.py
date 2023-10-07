from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

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
