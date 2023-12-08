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
df = pd.read_csv("fake_job_posting.csv")
df = df.drop("job_id") # job_id = 0,1,2,... 学習価値なし

# 訓練データとテストデータへの分割
Fakedf = df[ df_['fraudulent'] == 1 ]
Realdf = df[ df_['fraudulent'] == 0 ]

test_X = train_test_split(Fakedf, testsize=100)

#================================
# モデルの構築
#================================