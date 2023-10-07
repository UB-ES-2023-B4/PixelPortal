from fastapi import Depends, FastAPI, HTTPException,Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import repository,models, schemas
from database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from utils import verify_password, create_access_token, create_refresh_token, get_hashed_password, production
app = FastAPI()
models.Base.metadata.create_all(bind=engine) # Creem la base de dades amb els models que hem definit a SQLAlchemy


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}