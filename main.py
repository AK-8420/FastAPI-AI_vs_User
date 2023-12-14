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
        print("学習済みモデル（tree_model.json）が見つかりませんでした。新しく生成しますか？今までの対戦履歴はすべて初期化されます。[Y/n]")
        
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
#    tree_model = AI.get_trained_model(data.train_X, data.train_y)
#    tree_model.save_model('tree_model.json')

    # データベース初期化
    db = SessionLocal()
    db.query(models.Quiz).delete()          # 古い問題文の削除
    db.query(models.Prediction).delete()    # 古い問題文に基づく予測結果の削除
    db.query(models.Record).delete()        # 古い問題文に基づく戦歴の削除

    # ランダム抽出された問題文の保存
    for index, quiz in data.quizdf.iterrows():
        quiz_dict = quiz.to_dict()
        CRUD.create_quiz(db, schemas.QuizCreate(**quiz_dict)) # アンパックして渡す

    # 事前予測結果の保存
    quizset = db.query(models.Quiz).all()   # すべての問題文
#    for i, p in enumerate(AI.get_predictions(tree_model, quizset)):
    for i, p in enumerate([random.randint(0,1)]*100): # デバッグ用
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
    quiz_id = random.randint(1, CRUD.get_quiz_count(db))
    quiz_data = CRUD.get_quiz(db, quiz_id=quiz_id)
    return {"quiz_id": quiz_id, "quiz": quiz_data}


# 特定の問題を閲覧
@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    # 存在するquiz_idか？
    if CRUD.get_quiz(db, quiz_id) == None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
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
    
    quiz_data = CRUD.get_quiz(db, quiz_id=record.quiz_id)

    # ユーザーの回答が正しいか判定
    if record.user_answer == "Real" and quiz_data.fraudulent == False:
        result_user = True
    elif record.user_answer == "Fake" and quiz_data.fraudulent == True:
        result_user = True
    else:
        result_user = False
        
    # AIの回答が正しいか判定
    if predicted == False and quiz_data.fraudulent == False:
        result_AI = True
    elif predicted == True and quiz_data.fraudulent == True:
        result_AI = True
    else:
        result_AI = False
    
    # 勝敗判定
    if result_user == True and result_AI == False:
        result_battle = "Win"
    elif result_user == False and result_AI == True:
        result_battle = "Lose"
    else:
        result_battle = "Draw"
    
    return {
        "result_battle": result_battle,
        "user_answer": record.user_answer,
        "AI_answer": "Fake" if predicted else "Real",
        "correct_answer": "Fake" if quiz_data.fraudulent else "Real"
    }

# ユーザー名を編集（クエリで渡す）
@app.put("/result/{result_id}", response_model=schemas.Record)
async def put_record(result_id: str, username: str, db: Session = Depends(get_db)):
    record = CRUD.get_record(db, result_id)
    if record == None:
        raise HTTPException(status_code=404, detail="Record not found")
    
    record = CRUD.update_record(db, result_id, username)
    return record


# 戦歴を削除
@app.delete("/result/{result_id}")
async def delete_record(result_id: str, db: Session = Depends(get_db)):
    record = CRUD.get_record(db, result_id)
    if record == None:
        raise HTTPException(status_code=404, detail="Record not found")
    
    CRUD.delete_record(db, result_id)
    return {"status": "success",}


# すべての戦歴を取得 (idは作成者以外には非公開)
@app.get("/result")
async def get_record_all(db: Session = Depends(get_db)):
    dict_records = []

    for record in db.query(models.Record).all() :
        record_dict = record.__dict__
        record_dict.pop('result_id', None)  # result_idを除外
        dict_records.append(record_dict)

    return dict_records