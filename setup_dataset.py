import copy
import pandas as pd
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from transformers import AutoModel

#================================
# エンコーダー
#================================
def int_convert(value):
    try:
        output = int(value)
        return output
    except ValueError:
        return np.nan
    
# required_experience
def encoder_experience(text):
    experience_levels = {
        "Not Applicable": 0,
        "Internship": 1,
        "Entry level": 2,
        "Associate": 3,
        "Mid-Senior level": 4,
        "Director": 5,
        "Executive": 6
    }
    return int_convert(experience_levels.get(text, np.nan))

# required_education
def encoder_education(text):
    education_levels = {
        "Unspecified": 0,
        "Some High School Coursework": 1,
        "High School or equivalent": 2,
        "Vocational - HS Diploma": 2,
        "Some College Coursework Completed": 3,
        "Associate Degree": 4,
        "Vocational - Degree": 5,
        "Certification": 5,
        "Bachelor's Degree": 5,
        "Professional": 6,
        "Master's Degree": 7,
        "Doctorate": 8
    }
    return int_convert(education_levels.get(text, np.nan))

def split_columns_salary(df: pd.DataFrame):
    df['salary_lower'] = df['salary_range'].str.split('-').str[0].apply(int_convert)
    df['salary_upper'] = df['salary_range'].str.split('-').str[1].apply(int_convert)
    df = df.drop('salary_range', axis=1)
    return df

def preprocessing(df):
    # 要求経歴レベルを、文字列から数値に変換
    df['required_experience'] = df['required_experience'].apply(encoder_experience)
    df['required_education'] = df['required_education'].apply(encoder_education)

    # 給料範囲を上限と下限の2つのカラムに分ける
    df = split_columns_salary(df)

    # 不要な列の削除
    selected_columns = ['company_profile', 'description', 'benefits', 'required_experience', 'required_education', 'salary_lower', 'salary_upper']
    text_columns = ['company_profile', 'description', 'benefits']
    processed_df = copy.deepcopy(df[selected_columns])

    # 学習済みembeddingsモデルを外部からダウンロード
    embedding_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-small-en', trust_remote_code=True) # trust_remote_code is needed to use the encode method
    # GPUが使えたら使う
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    embedding_model.to(device)
    
    # 文字列をembedding
    for tc in text_columns:
        print(f"Now embedding {tc}...")
        embeddings = embedding_model.encode(processed_df[tc].fillna(''))
        print(f"{tc} is encoded.")

        # 行列の各列をDataFrameの新たなカラムとして保存
        columns = []
        for i in range(embeddings.shape[1]):
                columns.append(f'{tc}_{i}')
        emb_df = pd.DataFrame(embeddings, columns=columns)
        processed_df = pd.concat([processed_df, emb_df], axis=1)

        processed_df = processed_df.drop(tc, axis=1)
    
    return processed_df


#================================
# データセット管理クラス
#================================
class Dataset:
    def __init__(self):
        df = pd.read_csv("./fake_job_postings.csv")
        df = df.drop("job_id", axis=1) # job_id = 0,1,2,... 学習価値なし

        # 偽文書と本物文書
        Fakedf = df[ df['fraudulent'] == 1 ]
        Realdf = df[ df['fraudulent'] == 0 ]

        # テストデータのランダム抽出 (偽文書割合50%)
        detaset_Fake, quiz_Fake = train_test_split(Fakedf, test_size=50)
        detaset_Real, quiz_Real = train_test_split(Realdf, test_size=50)

        # テストデータをランダムシャッフルして保存
        quizdf = pd.concat([quiz_Real, quiz_Fake])
        self.quizdf = quizdf.sample(frac=1).reset_index(drop=True)

        # 訓練データもランダムシャッフル
        traindf = pd.concat([detaset_Fake, detaset_Real])
        traindf = traindf.sample(frac=1).reset_index(drop=True)

        self.train_y = traindf['fraudulent']

        # 訓練データの前処理
        train_X = traindf.drop('fraudulent', axis=1)
        self.train_X = preprocessing(train_X)