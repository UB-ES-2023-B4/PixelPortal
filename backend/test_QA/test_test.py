from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import Base

from fastapi.testclient import TestClient
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine)


# THIS
app.dependency_overrides[get_db] = override_get_db
# THIS

client = TestClient(app)

API_URL = "http://localhost:8000"

def test_register_user1():
    user_data = {
        "nombre": "testuser", 
        "email": "test@example.com", 
        "contrasena": "testpassword"
        }
    response = client.post(f"{API_URL}/usuario/", json=user_data)
    assert response.status_code == 200, response.json()