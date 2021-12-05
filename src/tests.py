import pytest
from controller import app


@pytest.fixture
def client():
    return app.test_client


def test_creating_user(client):
    response = client.get('/')
    print(response)
    assert b'Dzuske' in response.data
