from sqlalchemy import and_
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

from sqlalchemy.orm import Session
import models
import schemas


def create_user(db: Session, user: schemas.UsuarioCreate):
    hashed_password = get_password_hash(user.contrasena)
    db_user = models.Usuario(
        nombre=user.nombre,
        email=user.email,
        contrasena=hashed_password,  # Guarda la contraseña hasheada
        descripcion=user.descripcion,
        imagen_perfil_url = user.imagen_perfil_url # Puede ser None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()

def get_all_user(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Usuario).offset(skip).limit(limit).all()
def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.Usuario).filter(models.Usuario.nombre== username).first()

def update_account(db: Session, username: str, account: schemas.Usuario):
    db_user = db.query(models.Usuario).filter(models.Usuario.nombre == username).first()
    if not db_user:
        return None
    for var, value in vars(account).items():
        if value is not None:
            setattr(db_user, var, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def change_password(db:Session, user: models.Usuario, new_password: schemas.UsuarioChangePassword):
    user.contraseña = new_password.new_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def crear_publicacion(db: Session, publicacion: schemas.PublicacionCreate, usuario_id: int):
    db_publicacion = models.Publicacion(**publicacion.dict(), usuario_id=usuario_id)
    db.add(db_publicacion)
    db.commit()
    db.refresh(db_publicacion)
    return db_publicacion

def get_post(db: Session, post_id: int):
    return db.query(models.Publicacion).filter(models.Publicacion.id == post_id).first()

def obtener_publicaciones(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Publicacion).offset(skip).limit(limit).all()

def delete_publication(db: Session, publication_id: int):
    db_publication = db.query(models.Publicacion).filter(models.Publicacion.id == publication_id).first()
    if not db_publication:
        return None

    db.query(models.Comentario).filter(models.Comentario.publicacion_id == publication_id).delete() #Borramos los comentarios
    db.query(models.Like).filter(models.Like.publicacion_id == publication_id).delete()
    db.delete(db_publication)
    db.commit()

    return db_publication

def crear_comentario(db: Session, comentario: schemas.ComentarioCreate, usuario_actual: models.Usuario):
    db_comentario = models.Comentario(
        usuario_id=usuario_actual.id,
        publicacion_id=comentario.publicacion_id,
        contenido=comentario.contenido
    )
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

def crear_like(db: Session, like: schemas.LikeCreate, usuario_actual: models.Usuario):

    like_exist = db.query(models.Like).filter(and_(models.Like.publicacion_id == like.publicacion_id, models.Like.usuario_id == like.usuario_id)).all()
    if like_exist: #Ese like ya existe
        like_exist = None
        return like_exist
    db_like = models.Like(usuario_id=like.usuario_id, publicacion_id=like.publicacion_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def get_users_liked_a_post(db: Session, publication_id: int):
    # Obtener todos los likes para la publicación con la ID dada
    db_likes = db.query(models.Like).filter(models.Like.publicacion_id == publication_id).all()

    # Obtener los usuarios correspondientes a esos likes
    users_likes = []
    for like in db_likes:
        user = db.query(models.Usuario).filter(models.Usuario.id == like.usuario_id).first()
        if user:
            users_likes.append(user)

    return users_likes

def get_posts_liked_by_user(db: Session, user_id: int):
    # Obtener todos los likes para la publicación con la ID dada
    db_likes = db.query(models.Like).filter(models.Like.usuario_id == user_id).all()

    # Obtener los usuarios correspondientes a esos likes
    publication_likes = []
    for like in db_likes:
        publication = db.query(models.Publicacion).filter(models.Publicacion.id == like.publicacion_id).first()
        if publication:
            publication_likes.append(publication)

    return publication_likes

def get_all_likes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Like).offset(skip).limit(limit).all()

def delete_like(db: Session, like: schemas.Like):
    db_like = db.query(models.Like).filter(and_(models.Like.publicacion_id == like.publicacion_id, models.Like.usuario_id == like.usuario_id)).first()
    if not db_like:
        return None
    db.query(models.Like).filter(and_(models.Like.publicacion_id == like.publicacion_id, models.Like.usuario_id == like.usuario_id)).delete()
    db.commit()

    return db_like


###### METODOS RELACIONADOS CON SEGUIDORES ################

def follow_user(db: Session, user_id: int, follower_id: int):
   
    if not db.query(models.Usuario).filter(models.Usuario.id == user_id).first():
        return None
    if not db.query(models.Usuario).filter(models.Usuario.id == follower_id).first():
        return None
    
    if db.query(models.Seguidor).filter(models.Seguidor.seguidor_id == follower_id, models.Seguidor.seguido_id == user_id).first():
        return None

    new_follow = models.Seguidor(seguidor_id=follower_id, seguido_id=user_id)
    db.add(new_follow)
    db.commit()
    return new_follow


def unfollow_user(db: Session, user_id: int, follower_id: int):
    follow_relation = db.query(models.Seguidor).filter(models.Seguidor.seguidor_id == follower_id, models.Seguidor.seguido_id == user_id).first()
    if not follow_relation:
        return None

    db.delete(follow_relation)
    db.commit()
    return follow_relation


def get_followers(db: Session, user_id: int):
    followers = db.query(models.Seguidor).filter(models.Seguidor.seguido_id == user_id).all()
    return [follower.seguidor for follower in followers]


def get_following(db: Session, user_id: int):
    following = db.query(models.Seguidor).filter(models.Seguidor.seguidor_id == user_id).all()
    return [follow.seguido for follow in following]


