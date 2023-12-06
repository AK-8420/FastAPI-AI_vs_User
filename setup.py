import sqlite3

db_file_name = "history.db"

# SQLiteデータベースに接続（ファイルが存在しない場合は新規作成される）
conn = sqlite3.connect(db_file_name)
cursor = conn.cursor()

# 戦歴テーブルの作成
cursor.execute('''CREATE TABLE IF NOT EXISTS battle_records (
    id TEXT PRIMARY KEY,
    datetime INTEGER NOT NULL,
    username TEXT,
    win INTEGER NOT NULL
)''')

conn.commit()
conn.close()

print(f"データベース '{db_file_name}' が作成されました")