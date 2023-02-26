import pytest
from app import app, translate_en2vi
import time

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_translate_en2vi_cache_lock(client):
    # First request: should compute translation
    start_time = time.monotonic()
    response1 = client.post('/translate/en2vi', json={'en_text': 'Hello world!'})
    end_time = time.monotonic()
    assert response1.status_code == 200
    assert 'Xin chào thế giới' in response1.json['vi_text']
    assert end_time - start_time >= 2  # Ensure translation took some time

    # Second request with same input: should use cached result
    start_time = time.monotonic()
    response2 = client.post('/translate/en2vi', json={'en_text': 'Hello world!'})
    end_time = time.monotonic()
    assert response2.status_code == 200
    assert 'Xin chào thế giới' in response2.json['vi_text']
    assert end_time - start_time < 1  # Ensure response is fast (due to caching)

    # Third request with different input: should compute new translation
    start_time = time.monotonic()
    response3 = client.post('/translate/en2vi', json={'en_text': 'This is a test.'})
    end_time = time.monotonic()
    assert response3.status_code == 200
    assert 'Đây là một bài kiểm tra' in response3.json['vi_text']
    assert end_time - start_time >= 2  # Ensure translation took some time
