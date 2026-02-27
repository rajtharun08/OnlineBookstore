import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal

@pytest.fixture(scope="module")
def client():
    """Provides a TestClient for the suite."""
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db():
    """Provides a database session for cleanup."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()