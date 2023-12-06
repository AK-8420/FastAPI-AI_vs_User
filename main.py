from fastapi import FastAPI, HTTPException
app = FastAPI()

# test data
data = {
    str(i): f"item{i}" for i in range(1, 81)
}

@app.get("/")
async def root():
 return {"Hello": "World",}

@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str):
    if quiz_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"quiz_id": quiz_id, "quiz": data[quiz_id]}

@app.post("/quiz/{quiz_id}")
async def post_answer(quiz_id: str, answer: str, username: str = "Unknown user"):
    if quiz_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    if not (answer == 'Real' or answer == 'Fake'):
        raise HTTPException(status_code=422, detail="Invalid answer was submitted.")
    
    # 新しい戦歴を作成
    result_hash_id = "random-hash-string"
    date = "unix date"
    isCorrect = 1 # True=1, False=0
    
    # ここでDBへ保存
    # ...

    return {"result_hash_id": result_hash_id}