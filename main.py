import random

import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import CRUD, models, schemas
from setup_database import SessionLocal
from setup_dataset import quiz, quiz_solution

app = FastAPI()

# 各エンドポイントの処理前後のデータベース接続管理
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


# ランダムに問題を出題
@app.get("/quiz")
async def get_quiz():
    quiz_id = random.randint(1, 100)
    quiz_data = quiz.iloc[quiz_id - 1].to_dict()
    return {"quiz_id": quiz_id, "quiz": quiz_data}


# 特定の問題を閲覧
@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str):
    quiz_id = is_valid_quiz_id(quiz_id)
    quiz_data = quiz.iloc[quiz_id - 1].to_dict()
    return {"quiz_id": quiz_id, "quiz": quiz_data}


# ユーザーの回答を送信
@app.post("/quiz", response_model=schemas.Record)
async def post_answer(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    if CRUD.get_prediction(db, record.quiz_id) == None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if not (record.user_answer == 'Real' or record.user_answer == 'Fake'):
        raise HTTPException(status_code=400, detail="Invalid answer. Please submit 'Real' or 'Fake' in string format.")

    return CRUD.create_record(db=db, record_data=record_data)


# クイズの結果を取得
@app.get("/result/{result_id}")
async def get_result(result_id: str, db: Session = Depends(get_db)):
    record = CRUD.get_record(db, result_id)
    if record == None:
        raise HTTPException(status_code=404, detail="Record not found")

    predicted = record.AI_answer.predicted_as
    if predicted == None:
        raise HTTPException(status_code=404, detail="Prediction by AI not found")
        
    if record.user_answer == "Real" and quiz_solution[record.quiz_id - 1] == 0:
        isCorrect = True
    elif record.user_answer == "Fake" and quiz_solution[record.quiz_id - 1] == 1:
        isCorrect = True
    else:
        isCorrect = False
    
    result_battle = "win"
    
    return {
        "result_battle": result_battle,
        "result_user": isCorrect,
        "result_AI": predicted
    }