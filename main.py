import time
import uuid
import pandas as pd
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

import CRUD, models, schemas
from setup_database import SessionLocal, engine
from setup_dataset import quiz, quiz_solution

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# バリデーション関数
def is_valid_quiz_id(quiz_id: str):
    try:
        converted_id = int(quiz_id)
        if converted_id not in range(1, 101):
            raise HTTPException(status_code=404, detail="Index out of range (1 - 100)")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid index")
    return converted_id


@app.get("/")
async def root():
 return {"Hello": "World",}


@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str):
    quiz_id = is_valid_quiz_id(quiz_id)
    
    # DataFrameの行を辞書に変換
    quiz_data = quiz.iloc[quiz_id - 1].to_dict()

    return {"quiz_id": quiz_id, "quiz": quiz_data}


@app.post("/quiz/{quiz_id}")
async def post_answer(quiz_id: str, answer: str, username: str = "Unknown user"):
    quiz_id = is_valid_quiz_id(quiz_id)
    if not (answer == 'Real' or answer == 'Fake'):
        raise HTTPException(status_code=400, detail="Invalid answer. Please submit 'Real' or 'Fake' in string format.")
    
    # 新しい戦歴を作成
    result_id = uuid.uuid4()
    record = {
        "id": result_id,
        "quiz_id": quiz_id,
        "created_at": int(time.time()), # UNIX datetime
        "username": username,
        "user_answer": answer
    }
    
    # データベースに保存
    # ...

    return {"result_id": result_id}


@app.get("/result/{result_id}")
async def get_result(result_id: str):
    temporarytable = {
        "random-hash-string": True
    }
    if result_id not in temporarytable:
        raise HTTPException(status_code=404, detail="Record not found")
        
    # 回答を採点
    r = { # 本来はここでデータベースから戦歴を取得
        "quiz_id": 1,
        "user_answer": "Real"
    }
    if r["user_answer"] == "Real" and quiz_solution[r["quiz_id"] - 1] == 0:
        isCorrect = True
    elif r["user_answer"] == "Fake" and quiz_solution[r["quiz_id"] - 1] == 1:
        isCorrect = True
    else:
        isCorrect = False
    
    return {
        "result_id": result_id,
        "result_user": temporarytable[result_id],
        "result_AI": temporarytable[result_id]
    }