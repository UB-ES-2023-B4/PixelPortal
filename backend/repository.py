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

def create_user(db: Session, user: schemas.UsuarioCreate):
    db_user = models.Usuario(
        nombre=user.nombre,
        email=user.email,
        contrasena=user.contrasena,  # ¡Asegúrate de hashear la contraseña antes de guardarla!
        descripcion=user.descripcion
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


