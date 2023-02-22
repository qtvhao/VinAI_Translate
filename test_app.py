import pytest
from app import app, translate_en2vi

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_translate_en2vi(client):
    response = client.get('/translate/en2vi?text=Hello%20world!')
    assert response.status_code == 200
    assert response.json['translation'] == 'Xin chào thế giới!'

    response = client.get('/translate/en2vi?text=This%20is%20a%20test.&max_length=10')
    assert response.status_code == 200
    assert response.json['translation'] == 'Đây là một...'

    response = client.get('/translate/en2vi?text=')
    assert response.status_code == 400
    assert response.json['error'] == 'No text provided'

    response = client.get('/translate/en2vi?text=Hello%20world!&invalid_param=123')
    assert response.status_code == 400
    assert response.json['error'] == 'Invalid parameter: invalid_param'
