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

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuario/", response_model=schemas.Usuario)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = repository.create_user(db, user)
    return db_user
