import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database import Base

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()  # 테스트가 끝나면 롤백을 수행하여 데이터베이스를 초기 상태로 되돌림
        session.close()
        
@pytest.fixture(scope="function")
def test_client(db):
    from fastapi.testclient import TestClient
    from main import app, get_db
    app.dependency_overrides[get_db] = db  # FastAPI 의존성을 테스트용 세션으로 오버라이드
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)  # 테스트용 테이블 삭제