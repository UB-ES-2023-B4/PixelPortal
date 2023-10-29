from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from schemas import UserSchema
from models import User

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserSchema)
def create_user(user_data: UserSchema, database_session: Session = Depends(get_db)):
    db_user = User(email=user_data.email)
    database_session.add(db_user)
    database_session.commit()

    return db_user