import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.session import Base, get_db
from unittest.mock import patch

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Tharun%4008@localhost:5432/order_test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_customer_user():
    return {"email": "buyer@test.com", "role": "customer", "id": str(uuid.uuid4()),"token": "fake-jwt-token"}

@pytest.fixture
def mock_book_api():
    with patch("httpx.AsyncClient.get") as mock_get, \
         patch("httpx.AsyncClient.put") as mock_put:
        yield {"get": mock_get, "put": mock_put}

def test_health_check(client):
    response = client.get("/health") 
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}