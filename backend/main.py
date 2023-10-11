from fastapi import Depends, FastAPI, HTTPException,Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import repository,models, schemas
from database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from utils import verify_password, create_access_token, create_refresh_token, get_hashed_password #production
import models
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine  # Asegúrate de que tu módulo de base de datos está importado correctamente
import models, schemas, repository  # Asegúrate de que tu
app = FastAPI()
models.Base.metadata.create_all(bind=engine) # Creem la base de dades amb els models que hem definit a SQLAlchemy
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from repository import create_user
from models import Usuario as DBUsuario
from schemas import UsuarioCreate, Usuario
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, repository
from dependencies import get_db, verify_password, create_access_token, get_current_user
from datetime import timedelta
from repository import get_user_by_email

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#Registro
@app.post("/usuario/")
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = repository.create_user(db, user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": schemas.Token(access_token=access_token, token_type="bearer"), "user": db_user}

#Login
@app.post("/login")
async def login(usuario: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    db_user = db.query(DBUsuario).filter(DBUsuario.email == usuario.email).first()
    if db_user is None or not verify_password(usuario.contrasena, db_user.contrasena):
        return {"detail": "Usuario no registrado o credenciales inválidas"}
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


#Obtener usuario por ID
@app.get("/usuario/{user_id}", response_model=schemas.Usuario)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user



@app.get("/users/me/", response_model=schemas.Usuario)
async def read_users_me(current_user: models.Usuario = Depends(get_current_user)):
    return current_user