import pandas as pd
from fastapi import FastAPI, HTTPException
app = FastAPI()

df = pd.read_csv("quiz.csv")
quiz = df.drop("fraudulent", axis=1)
quiz_solution = df["fraudulent"]

# test data
data = {
    str(i): f"item{i}" for i in range(1, 101)
}
data2 = {
    "random-hash-string": "Correct"
}
data3 = {
    "random-hash-string": "Wrong"
}

@app.get("/")
async def root():
 return {"Hello": "World",}

@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str):
    try:
        id = int(quiz_id)
        if id not in range(1, 101):
            raise HTTPException(status_code=404, detail="Index out of range (1 - 100)")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid index")
    
    # DataFrameの行を辞書に変換
    quiz_data = quiz.iloc[id-1].to_dict()
    # NaNをnullに変換
    for key, value in quiz_data.items():
        if pd.isna(value):
            quiz_data[key] = "null"

    return {"quiz_id": id, "quiz": quiz_data}

@app.post("/quiz/{quiz_id}")
async def post_answer(quiz_id: str, answer: str, username: str = "Unknown user"):
    if int(quiz_id) not in range(1, 101):
        raise HTTPException(status_code=404, detail="Index out of range")
    if not (answer == 'Real' or answer == 'Fake'):
        raise HTTPException(status_code=400, detail="Invalid answer. Please submit 'Real' or 'Fake' in string.")
    
    # 新しい戦歴を作成
    result_hash_id = "random-hash-string"
    date = "unix date"
    isCorrect = 1 # True=1, False=0
    
    # ここでDBへ保存
    # ...

    return {"result_hash_id": result_hash_id}

@app.get("/result/{result_hash_id}")
async def get_result(result_hash_id: str):
    if result_hash_id not in data2:
        raise HTTPException(status_code=404, detail="Record not found")
    
    return {"result_hash_id": result_hash_id, "result_user": data2[result_hash_id], "result_AI": data3[result_hash_id]}