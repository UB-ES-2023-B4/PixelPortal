from sqlalchemy import Boolean, MetaData, Column, ForeignKey, Integer, String, Date, Float, Enum, UniqueConstraint, Table,LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from database import Base
from sqlalchemy.sql import func 
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Table, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'Usuarios'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    contrasena = Column(String(100), nullable=False)
    descripcion = Column(String(100), nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    imagen_perfil_url = Column(String(255), nullable=True)

class Publicacion(Base):
    __tablename__ = 'Publicaciones'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey('Usuarios.id'), nullable=False)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    
    usuario = relationship("Usuario", back_populates="publicaciones")
    
Usuario.publicaciones = relationship("Publicacion", order_by=Publicacion.id, back_populates="usuario")

class Comentario(Base):
    __tablename__ = 'Comentarios'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    usuario_id = Column(BigInteger, ForeignKey('Usuarios.id'), nullable=False)
    publicacion_id = Column(BigInteger, ForeignKey('Publicaciones.id'), nullable=False)
    contenido = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    
    usuario = relationship("Usuario", back_populates="comentarios")
    publicacion = relationship("Publicacion", back_populates="comentarios")
    
Usuario.comentarios = relationship("Comentario", order_by=Comentario.id, back_populates="usuario")
Publicacion.comentarios = relationship("Comentario", order_by=Comentario.id, back_populates="publicacion")

class Like(Base):
    __tablename__ = 'Likes'
    
    usuario_id = Column(BigInteger, ForeignKey('Usuarios.id'), primary_key=True)
    publicacion_id = Column(BigInteger, ForeignKey('Publicaciones.id'), primary_key=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    
    usuario = relationship("Usuario", back_populates="likes")
    publicacion = relationship("Publicacion", back_populates="likes")
    
Usuario.likes = relationship("Like", order_by=Like.fecha_creacion, back_populates="usuario")
Publicacion.likes = relationship("Like", order_by=Like.fecha_creacion, back_populates="publicacion")

class Seguidor(Base):
    __tablename__ = 'Seguidores'
    
    seguidor_id = Column(BigInteger, ForeignKey('Usuarios.id'), primary_key=True)
    seguido_id = Column(BigInteger, ForeignKey('Usuarios.id'), primary_key=True)
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    
    seguidor = relationship("Usuario", foreign_keys=[seguidor_id], back_populates="siguiendo")
    seguido = relationship("Usuario", foreign_keys=[seguido_id], back_populates="seguidores")
    
Usuario.siguiendo = relationship("Seguidor", foreign_keys=[Seguidor.seguidor_id], back_populates="seguidor")
Usuario.seguidores = relationship("Seguidor", foreign_keys=[Seguidor.seguido_id], back_populates="seguido")