import random
import os
import sys

import xgboost as xgb
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import CRUD, models, schemas, AI
from setup_database import SessionLocal, engine
from setup_dataset import Dataset


# サーバー再起動のたびにモデル構築を防止
if os.path.exists('tree_model.json'):
    # トレーニング済モデルを取得
    tree_model = xgb.Booster()
    tree_model.load_model('tree_model.json')
    
else:
    while True:
        print("tree_model.jsonが見つかりませんでした。データベースを初期化して、新しく生成しますか？[Y/n]")
        
        # ユーザーの入力を待つ
        answer = input().strip().lower() # 空白文字削除と小文字化
        if answer == 'y':
            print("新しいモデルを生成します。")
            break
        elif answer == 'n':
            print("プログラムを終了します。")
            sys.exit(0) # uvicornの終了はされない
        else:
            print("無効な入力です。")

    # データベースにテーブル作成
    models.Base.metadata.create_all(bind=engine)

    # 訓練データと本番データの作成
    data = Dataset()

    # モデル構築
    tree_model = AI.get_trained_model(data.train_X, data.train_y)
    tree_model.save_model('tree_model.json')

    # データベース初期化
    db = SessionLocal()
    db.query(models.Quiz).delete()          # 古い問題文の削除
    db.query(models.Prediction).delete()    # 古い問題文に基づく予測結果の削除
    db.query(models.Record).delete()        # 古い問題文に基づく戦歴の削除

    # ランダム抽出された問題文の保存
    for quiz in data.quizdf.iterrows():
        CRUD.create_quiz(db, schemas.QuizCreate(quiz))

    # 事前予測結果の保存
    quizset = db.query(models.Quiz).all()   # すべての問題文
    for i, p in enumerate(AI.get_predictions(tree_model, quizset)):
        prediction_data = schemas.PredictionCreate(quiz_id=i, predicted_as=p)
        CRUD.create_prediction(db, prediction_data)
    db.close()

# APIインスタンス作成
app = FastAPI()


# 各エンドポイントの処理前後のデータベース接続管理
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
async def root():
 return {"Hello": "World",}


# ランダムに問題を出題
@app.get("/quiz")
async def get_quiz(db: Session = Depends(get_db)):
    quiz_id = random.randint(0, CRUD.get_quiz_count(db) - 1)
    quiz_data = CRUD.get_quiz(db, quiz_id=quiz_id)
    return {"quiz_id": quiz_id, "quiz": quiz_data}


# 特定の問題を閲覧
@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: str, db: Session = Depends(get_db)):
    # バリデーション
    try:
        converted_id = int(quiz_id)
        if converted_id not in range(CRUD.get_quiz_count(db)):
            raise HTTPException(status_code=404, detail="Index is out of range")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid index")
    
    quiz_data = CRUD.get_quiz(db, quiz_id=quiz_id)
    return {"quiz_id": quiz_id, "quiz": quiz_data}


# ユーザーの回答を送信
@app.post("/quiz", response_model=schemas.Record)
async def post_answer(record: schemas.RecordCreate, db: Session = Depends(get_db)):
    if CRUD.get_quiz(db, record.quiz_id) == None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    if not (record.user_answer == 'Real' or record.user_answer == 'Fake'):
        raise HTTPException(status_code=400, detail="Invalid answer. Please submit 'Real' or 'Fake' in string format.")

    return CRUD.create_record(db=db, record_data=record)


# クイズの結果を取得
@app.get("/result/{result_id}")
async def get_result(result_id: str, db: Session = Depends(get_db)):
    record = CRUD.get_record(db, result_id)
    if record == None:
        raise HTTPException(status_code=404, detail="Record not found")

    predicted = record.AI_answer.predicted_as
    if predicted == None:
        raise HTTPException(status_code=404, detail="Prediction by AI not found")
    
    # ユーザーの回答が正しいか判定
    if record.user_answer == "Real" and data.solutions[record.quiz_id - 1] == 0:
        isCorrect = True
    elif record.user_answer == "Fake" and data.solutions[record.quiz_id - 1] == 1:
        isCorrect = True
    else:
        isCorrect = False
    
    # ここで勝敗判定する
    result_battle = "win"
    
    return {
        "result_battle": result_battle,
        "result_user": isCorrect,
        "result_AI": predicted
    }