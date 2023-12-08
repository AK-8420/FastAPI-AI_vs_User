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
    if int(quiz_id) not in range(1, 101):
        raise HTTPException(status_code=404, detail="Index out of range")
    return {"quiz_id": int(quiz_id), "quiz": data[quiz_id]}

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