from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_get_collectID_1():
    quiz_id = 1
    response = client.get(f"/quiz/{quiz_id}")
    assert response.status_code == 200
    assert response.json() == {
        "quiz_id": str(quiz_id),
        "quiz": f"item{quiz_id}"
    }

def test_get_collectID_2():
    quiz_id = 100
    response = client.get(f"/quiz/{quiz_id}")
    assert response.status_code == 200
    assert response.json() == {
        "quiz_id": str(quiz_id),
        "quiz": f"item{quiz_id}"
    }

def test_get_wrongID():
    quiz_id = -1
    response = client.get(f"/quiz/{quiz_id}")
    assert response.status_code == 404

def test_post_collectID_1():
    quiz_id = 1
    response = client.post(f"/quiz/{quiz_id}?answer=Real")
    assert response.status_code == 200
    assert response.json() == {
        "result_hash_id": "random-hash-string"
    }

def test_post_collectID_2():
    quiz_id = 100
    response = client.post(f"/quiz/{quiz_id}?answer=Fake")
    assert response.status_code == 200
    assert response.json() == {
        "result_hash_id": "random-hash-string"
    }


def test_post_collectFormat_1():
    response = client.post(f"/quiz/1?answer=Fake")
    assert response.status_code == 200
    assert response.json() == {
        "result_hash_id": "random-hash-string"
    }
    

def test_post_collectFormat_2():
    response = client.post(f"/quiz/1?answer=Real")
    assert response.status_code == 200
    assert response.json() == {
        "result_hash_id": "random-hash-string"
    }

def test_post_wrongID():
    quiz_id = -1
    response = client.post(f"/quiz/{quiz_id}?answer=Fake")
    assert response.status_code == 404
    

def test_post_wrongFormat():
    response = client.post(f"/quiz/1?answer=aaa")
    assert response.status_code == 400