import pandas as pd
from sklearn.model_selection import train_test_split


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

# 訓練データ
train_X = pd.concat([train_X_Real, train_X_Fake])
train_y = pd.concat([train_y_Real, train_y_Fake])

# テストデータ
testdf = pd.concat([test_Real, test_Fake])
shuffled_df = testdf.sample(frac=1).reset_index(drop=True) #ランダムシャッフル
quiz = shuffled_df.drop("fraudulent", axis=1)        # 問題文
quiz_solution = shuffled_df["fraudulent"].to_numpy() # 解答

print(f"Test data is created.")

#================================
# モデルの構築
#================================