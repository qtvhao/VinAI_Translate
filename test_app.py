import pytest
from app import app, translate_en2vi

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_translate_en2vi(client):
    response = client.post('/translate/en2vi', json={'en_text': 'Hello world!'})
    assert response.status_code == 200
    assert response.json['vi_text'] == 'Xin chào thế giới!'

    response = client.post('/translate/en2vi', json={'en_text': 'This is a test.', 'max_length': 10})
    assert response.status_code == 200
    assert response.json['vi_text'] == 'Đây là một bài kiểm tra.'
