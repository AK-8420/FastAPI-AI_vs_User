from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["AI_accuracy"], float)
    assert isinstance(response_json["Users_accuracy"], float)

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
            "answer": "Real",
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
            "answer": "Real",
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
            "answer": "Fake", # Real is already tested
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
            "answer": "Real",
            "username": "test"
        }
    )
    assert response.status_code == 404

def test_post_wrongFormat():
    response = client.post(
        "/quiz",
        json={
            "quiz_id": 1,
            "answer": "hogehoge",
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
            "answer": "Fake",
            "username": "test"
        }
    )
    response_json = response.json()
    hash_id = response_json["result_id"]

    response = client.get(f"/result/{hash_id}")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["Battle_result"], str)

def test_get_result_wrongID():
    hash_id = "not-exist-ID"
    response = client.get(f"/result/{hash_id}")
    assert response.status_code == 404


def test_get_results():
    response = client.get(f"/result")
    assert response.status_code == 200


def test_get_results_by_username():
    response = client.post(
        "/quiz",
        json={
            "quiz_id": 1,
            "answer": "Fake",
            "username": "test"
        }
    )
    
    response = client.get("/result/fillter/test")
    response_json = response.json()
    assert response.status_code == 200
    
    # 全要素でusernameが"test"であることを確認
    for item in response_json:
        assert item["username"] == "test"


def test_get_results_by_wrong_username():
    response = client.get(f"/result/fillter/Not-Exist-Username")
    response_json = response.json()
    assert response_json == []


#==================================
# 戦歴編集
#==================================
def test_put_record():
    response = client.post(
        "/quiz",
        json={
            "quiz_id": 1,
            "answer": "Fake",
            "username": "hogehogeeeeeee"
        }
    )
    response_json = response.json()
    hash_id = response_json["result_id"]

    response = client.put(f"/result/{hash_id}?username=fugafuga")
    assert response.status_code == 200
    
    response = client.get(f"/result")
    response_json = response.json()
    for item in response_json:
        assert item["username"] != "hogehogeeeeeee"
    


#==================================
# 戦歴削除
#==================================
def test_delete_record_collectID():
    response = client.post(
        "/quiz",
        json={
            "quiz_id": 1,
            "answer": "Fake",
            "username": "test"
        }
    )
    response_json = response.json()
    hash_id = response_json["result_id"]

    response = client.delete(f"/result/{hash_id}")
    assert response.status_code == 200

    response = client.get(f"/result/{hash_id}")
    assert response.status_code == 404

def test_delete_record_wrongID():
    hash_id = "not-exist-ID"
    response = client.delete(f"/result/{hash_id}")
    assert response.status_code == 404