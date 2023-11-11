import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) + "\\backend")

from backend.main import app, models, get_db, get_current_user
from fastapi import Depends, HTTPException, status
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from backend.dependencies import SECRET_KEY, ALGORITHM
from backend.dependencies import get_user_by_email
import backend.schemas as schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def override_get_current_user(db: Session = Depends(override_get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@pytest.fixture(scope="function")
def test_client():
    models.Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    models.Base.metadata.drop_all(bind=engine)