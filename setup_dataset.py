import pandas as pd
from sklearn.model_selection import train_test_split

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

        # 問題文データのランダム抽出 (偽文書割合50%)
        detaset_Fake, quiz_Fake = train_test_split(Fakedf, test_size=50)
        detaset_Real, quiz_Real = train_test_split(Realdf, test_size=50)

        # 問題文データのランダムシャッフル
        quizdf = pd.concat([quiz_Real, quiz_Fake])
        shuffled_df = quizdf.sample(frac=1).reset_index(drop=True)

        self.problems = shuffled_df.drop("fraudulent", axis=1)   # 問題文  
        self.solutions = shuffled_df["fraudulent"].to_numpy()    # 解答

        # 訓練データとテストデータへの分割 (テストデータ25%)
        train_Fake, test_Fake = train_test_split(detaset_Fake)
        train_Real, test_Real = train_test_split(detaset_Real)
        traindf = pd.concat([train_Real, train_Fake])
        testdf = pd.concat([test_Real, test_Fake])
        traindf = traindf.sample(frac=1).reset_index(drop=True)
        testdf = testdf.sample(frac=1).reset_index(drop=True)

        train_X = testdf.drop('fraudulent', axis=1)
        self.train_y = testdf['fraudulent']
        test_X = testdf.drop('fraudulent', axis=1)
        self.test_y = testdf['fraudulent']

        # ここでデータ加工

        self.train_X = train_X
        self.test_X = test_X