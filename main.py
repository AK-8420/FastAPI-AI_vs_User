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