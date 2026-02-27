import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.base import Base
from app.core.dependencies import get_db
from app.core.security import create_access_token
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db")
def db_fixture():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def test_user(db):
    user = User(
        id=uuid4(),
        email="user@test.com",
        password_hash="fake_hashed_password", # Matches your model!
        role="customer"
    )
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def user_token(test_user):
    return create_access_token(data={"sub": str(test_user.id), "role": test_user.role})

@pytest.fixture
def test_admin(db):
    admin = User(
        id=uuid4(),
        email="admin@test.com",
        password_hash="fake_hashed_admin_password", 
        role="admin"
    )
    db.add(admin)
    db.commit()
    return admin

@pytest.fixture
def admin_token(test_admin):
    return create_access_token(data={"sub": str(test_admin.id), "role": test_admin.role})