from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def register_data():
    data = {
        'email': 'test@example.com',
        'login': 'test_dev',
        'password': 'test112233'
    }
    yield data
