import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split

db_file_name = "history.db"

#================================
# SQLiteデータベース作成
#================================
# データベースに接続（ファイルが存在しない場合は新規作成される）
conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()

# 戦歴テーブルの作成
cursor.execute('''CREATE TABLE IF NOT EXISTS battle_records (
    id TEXT PRIMARY KEY,
    quiz_id INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    username TEXT,
    user_answer INTEGER NOT NULL
)''')

conn.commit()
conn.close()
print(f"データベース '{db_file_name}' が作成されました")


#================================
# データ準備
#================================
df = pd.read_csv("./fake_job_postings.csv")
df = df.drop("job_id", axis=1) # job_id = 0,1,2,... 学習価値なし
df.fillna('null', inplace=True) # 空の文字列 -> null

# 偽文書と本物文書
Fakedf = df[ df['fraudulent'] == 1 ]
Realdf = df[ df['fraudulent'] == 0 ]

# 訓練データとテストデータへのランダム分割 (テストデータの偽文書割合50%)
train_X_Fake, test_Fake = train_test_split(Fakedf, test_size=50)
train_y_Fake = train_X_Fake['fraudulent']
train_X_Fake = train_X_Fake.drop('fraudulent', axis=1)

train_X_Real, test_Real = train_test_split(Realdf, test_size=50)
train_y_Real = train_X_Real['fraudulent']
train_X_Real = train_X_Real.drop('fraudulent', axis=1)

train_X = pd.concat([train_X_Real, train_X_Fake])
train_y = pd.concat([train_y_Real, train_y_Fake])

# 問題文データの作成
testdf = pd.concat([test_Real, test_Fake])
shuffled_df = testdf.sample(frac=1).reset_index(drop=True) #ランダムシャッフル
shuffled_df.to_csv('./quiz.csv', index=False, mode='w')

#================================
# モデルの構築
#================================