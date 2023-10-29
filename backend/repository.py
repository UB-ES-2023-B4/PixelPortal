from sqlalchemy.orm import Session
import models
import schemas
from dependencies import get_password_hash

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

def delete_publication(db: Session, publication_id : int):
    db_publication = db.query(models.Publicacion).filter(models.Publicacion.id == publication_id).first()
    if not db_publication:
        return None
    db.delete(db_publication)
    db.commit()
    return db_publication
