import time
import uuid
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi import FastAPI, HTTPException

app = FastAPI()

# DB接続用のセッションクラス定義
engine = create_engine(f"sqlite:///./history.db", echo=True)
sessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# 問題文読み込み
df = pd.read_csv("quiz.csv")
df.fillna('null', inplace=True) # 空の文字列 -> null

quiz = df.drop("fraudulent", axis=1)        # 問題文
quiz_solution = df["fraudulent"].to_numpy() # 解答

temporarytable = {
    "random-hash-string":True
}

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
    
    # 回答を採点
    if answer == "Real" and quiz_solution[quiz_id - 1] == 0:
        isCorrect = True
    elif answer == "Fake" and quiz_solution[quiz_id - 1] == 1:
        isCorrect = True
    else:
        isCorrect = False
    
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
    if result_id not in temporarytable:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return {
        "result_id": result_id,
        "result_user": temporarytable[result_id],
        "result_AI": temporarytable[result_id]
    }