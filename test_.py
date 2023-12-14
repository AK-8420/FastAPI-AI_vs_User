from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

#==================================
# 問題文取得
#==================================
def test_get_quiz():
    response = client.get(f"/quiz")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["quiz_id"], int)

def test_get_collectID_1():
    quiz_id = 1
    response = client.get(f"/quiz/{quiz_id}")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["quiz_id"], int)
    assert response_json["quiz_id"] == quiz_id

def test_get_collectID_2():
    quiz_id = 100
    response = client.get(f"/quiz/{quiz_id}")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["quiz_id"], int)
    assert response_json["quiz_id"] == quiz_id

def test_get_wrongID_1():
    quiz_id = -1
    response = client.get(f"/quiz/{quiz_id}")
    assert response.status_code == 404


def test_get_wrongID_2():
    quiz_id = "aaaa"
    response = client.get(f"/quiz/{quiz_id}")
    assert response.status_code == 422

#==================================
# 回答送信
#==================================
def test_post_collectID_1():
    quiz_id = 1
    response = client.post(
        "/quiz",
        json={
            "quiz_id": quiz_id,
            "user_answer": "Real",
            "username": "test"
        }
    )
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["result_id"], str)

def test_post_collectID_2():
    quiz_id = 100
    response = client.post(
        "/quiz",
        json={
            "quiz_id": quiz_id,
            "user_answer": "Real",
            "username": "test"
        }
    )
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["result_id"], str)

def test_post_collectFormat():
    response = client.post(
        "/quiz",
        json={
            "quiz_id": 1,
            "user_answer": "Fake", # Real is already tested
            "username": "test"
        }
    )
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["result_id"], str)

def test_post_wrongID():
    quiz_id = -1
    response = client.post(
        "/quiz",
        json={
            "quiz_id": quiz_id,
            "user_answer": "Real",
            "username": "test"
        }
    )
    assert response.status_code == 404

def test_post_wrongFormat():
    response = client.post(
        "/quiz",
        json={
            "quiz_id": 1,
            "user_answer": "hogehoge",
            "username": "test"
        }
    )
    assert response.status_code == 400


#==================================
# 戦歴取得
#==================================
def test_get_result_collectID():
    response = client.post(
        "/quiz",
        json={
            "quiz_id": 1,
            "user_answer": "Fake",
            "username": "test"
        }
    )
    response_json = response.json()

    hash_id = response_json["result_id"]
    response = client.get(f"/result/{hash_id}")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["result_battle"], str)

def test_get_result_wrongID():
    hash_id = "not-exist-ID"
    response = client.get(f"/result/{hash_id}")
    assert response.status_code == 404


def test_get_results():
    response = client.get(f"/result")
    assert response.status_code == 200