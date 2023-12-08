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

def test_get_wrongID():
    quiz_id = -1
    response = client.get(f"/quiz/{quiz_id}")
    assert response.status_code == 404

#==================================
# 回答送信
#==================================
def test_post_collectID_1():
    quiz_id = 1
    response = client.post(f"/quiz/{quiz_id}?answer=Real")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["result_hash_id"], str)

def test_post_collectID_2():
    quiz_id = 100
    response = client.post(f"/quiz/{quiz_id}?answer=Fake")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["result_hash_id"], str)

def test_post_collectFormat_1():
    response = client.post(f"/quiz/1?answer=Fake")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["result_hash_id"], str)
    
def test_post_collectFormat_2():
    response = client.post(f"/quiz/1?answer=Real")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["result_hash_id"], str)

def test_post_wrongID():
    quiz_id = -1
    response = client.post(f"/quiz/{quiz_id}?answer=Fake")
    assert response.status_code == 404

def test_post_wrongFormat():
    response = client.post(f"/quiz/1?answer=aaa")
    assert response.status_code == 400


#==================================
# 戦歴取得
#==================================
def test_get_result_collectID():
    hash_id = "random-hash-string"
    response = client.get(f"/result/{hash_id}")
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json["isCollect"], int)

def test_get_result_wrongID():
    hash_id = "not-exist-ID"
    response = client.get(f"/result/{hash_id}")
    response_json = response.json()
    assert response.status_code == 404