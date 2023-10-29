from datetime import timedelta
import re
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils import verify_password, create_access_token
from database import  engine  # Asegúrate de que tu módulo de base de datos está importado correctamente
from database import get_db
from models import Usuario as DBUsuario
import models
import schemas
import repository
from dependencies import get_current_user

#email pattern
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
app = FastAPI()
models.Base.metadata.create_all(bind=engine) # Creem la base de dades amb els models que hem definit a SQLAlchemy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "https://jolly-river-0df294303.4.azurestaticapps.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = repository.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#Registro
@app.post("/usuario/")
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_email = repository.get_user_by_email(db, user.email)
    if db_email:
        raise HTTPException(status_code=404, detail="Email already registered")

    db_user = repository.get_user_by_username(db, user.nombre)
    if db_user:
        raise HTTPException(status_code=404, detail="User already registered")
    if not user.email:
        raise HTTPException(status_code=400, detail="The 'email' field is required")
    if not user.nombre:
        raise HTTPException(status_code=400, detail="The 'name' field is required")
    if not user.contrasena:
        raise HTTPException(status_code=400, detail="The 'password' field is required")
    if not re.match(EMAIL_PATTERN, user.email):
        raise HTTPException(status_code=400, detail="the format of the field 'email' is not valid.")

    db_user = repository.create_user(db, user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    return {"access_token": schemas.Token(access_token=access_token, token_type="bearer"), "user": db_user}

#Login
@app.post("/login")
async def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    db_user = db.query(DBUsuario).filter(DBUsuario.email == usuario.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not in Database")
    if not verify_password(usuario.contrasena, db_user.contrasena):
        raise HTTPException(status_code=404, detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=usuario.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": db_user.nombre}

#Modificar perfil de usuario
@app.put('/usuario/{username}', summary="Put user", response_model=schemas.Usuario)
def update_account(username: str, account: schemas.UsuarioChange, db: Session = Depends(get_db)):
    db_account = repository.update_account(db, username, account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    return db_account
#Modificar la contraseña del usuario
@app.post("/usuario/change_pass")
def change_password(user: schemas.UsuarioChangePassword,db: Session = Depends(get_db)):
    # Verificar si el usuario existe
    db_user = repository.get_user_by_email(db, user.email)
    if user.current_password == user.new_password:
        raise HTTPException(status_code=404, detail="The new password is the same password")
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Autenticar al usuario
    if not verify_password(user.current_password, db_user.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_user = repository.change_password(db,db_user,user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)#Al cambiar la contraseña creamos un nuevo token
    access_token = create_access_token(
        subject=db_user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#Obtener usuario por ID
@app.get("/usuarios/", response_model=List[schemas.Usuario])
def read_user( db: Session = Depends(get_db)):
    db_user = repository.get_all_user(db)
    return db_user


@app.get("/usuario/{user_id}", response_model=schemas.Usuario)
def read_user_id(user_id: int, db: Session = Depends(get_db)):
    db_user = repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.get("/users/me/", response_model=schemas.Usuario)
async def read_users_me(current_user: models.Usuario = Depends(get_current_user)):
    return current_user

@app.post("/publicaciones/", response_model=schemas.Publicacion)
async def crear_publicacion(publicacion: schemas.PublicacionCreate, db: Session = Depends(get_db),current_user: models.Usuario = Depends(get_current_user) ):
    print(publicacion.tags)
    if not publicacion.titulo:
        raise HTTPException(status_code=400, detail="The 'titulo' field is required")
    if not publicacion.descripcion:
        raise HTTPException(status_code=400, detail="The 'descripcion' field is required")
    if not publicacion.usuario_nombre:
        raise HTTPException(status_code=400, detail="The 'usuario_nombre' field is required")
    if not publicacion.imagen_url:
        raise HTTPException(status_code=400, detail="The 'imagen_url' field is required")
    return repository.crear_publicacion(db=db, publicacion=publicacion, usuario_id=current_user.id)

@app.get("/publicaciones/", response_model=List[schemas.Publicacion])
def obtener_publicaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    publicaciones = repository.obtener_publicaciones(db, skip=skip, limit=limit)
    return publicaciones

@app.get("/publicaciones/{publication_id}", response_model=schemas.Publicacion)
def read_post(publication_id: int, db: Session = Depends(get_db)):
    db_post = repository.get_post(db, publication_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/publicacion/{publication_id}", response_model=schemas.Publicacion)
def delete_team(publication_id: int, db: Session = Depends(get_db)):
    db_publication = repository.delete_publication(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_publication
