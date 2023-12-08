import pandas as pd
from sklearn.model_selection import train_test_split
from fastapi import Depends
from sqlalchemy.orm import Session

import CRUD, schemas, models
from setup_database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

#================================
# データ準備
#================================
df = pd.read_csv("./fake_job_postings.csv")
df = df.drop("job_id", axis=1) # job_id = 0,1,2,... 学習価値なし
df.fillna('null', inplace=True) # 空の文字列 -> null

# 偽文書と本物文書
Fakedf = df[ df['fraudulent'] == 1 ]
Realdf = df[ df['fraudulent'] == 0 ]

# 問題文データのランダム抽出 (偽文書割合50%)
detaset_Fake, quiz_Fake = train_test_split(Fakedf, test_size=50)
detaset_Real, quiz_Real = train_test_split(Realdf, test_size=50)

# 問題文データのランダムシャッフル
quizdf = pd.concat([quiz_Real, quiz_Fake])
shuffled_df = quizdf.sample(frac=1).reset_index(drop=True)
quiz = shuffled_df.drop("fraudulent", axis=1)        # 問題文
quiz_solution = shuffled_df["fraudulent"].to_numpy() # 解答

print("Quiz data is created.")

# 訓練データとテストデータへの分割 (テストデータ25%)
train_Fake, test_Fake = train_test_split(detaset_Fake)
train_Real, test_Real = train_test_split(detaset_Real)
traindf = pd.concat([train_Real, train_Fake])
testdf = pd.concat([test_Real, test_Fake])
traindf = traindf.sample(frac=1).reset_index(drop=True)
testdf = testdf.sample(frac=1).reset_index(drop=True)
train_X = testdf.drop('fraudulent', axis=1)
train_y = testdf['fraudulent']
test_X = testdf.drop('fraudulent', axis=1)
test_y = testdf['fraudulent']

#================================
# モデルの構築
#================================
# 学習
# model = ...

# 予測
# predicted = model.predicted(test_X)
import random
predicted = [random.randint(0,1)]*100

# 予測結果の保存
db = SessionLocal()
db.query(models.Prediction).delete()
for p in predicted:
    if p == 1:
        prediction_data = schemas.PredictionCreate(predicted_as="Fake")
    else:
        prediction_data = schemas.PredictionCreate(predicted_as="Real")
    CRUD.create_prediction(db, prediction_data)
db.close()