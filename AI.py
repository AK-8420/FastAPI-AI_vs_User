import xgboost as xgb
import pandas as pd

from setup_dataset import preprocessing

# モデルの構築
def get_trained_model(train_X: pd.DataFrame, train_y: pd.DataFrame):
    print("Now training...")
    
    dtrain = xgb.DMatrix(data=train_X, label=train_y, enable_categorical=True) # カテゴリカルデータの分類は実験的機能

    # パラメータ決定の過程はXGBoost_test.ipynbを参照
    num_round = 20
    given_param = {
        'max_depth': 8,
        'objective' : 'binary:hinge'
    }
    trained_model = xgb.train(given_param, dtrain, num_round)

    print("Completed.")
    return trained_model

# 予測結果リストを返す（偽文書なら1、本物文書なら0）
def get_predictions(trained_model, quizset):
    print("Now getting predictions...")

    # クラスインスタンスのリストを辞書へ変換
    dict_list = []
    for quiz in quizset:
        quiz_dict = {column.name: getattr(quiz, column.name) for column in quiz.__table__.columns}
        dict_list.append(quiz_dict)
    
    df = pd.DataFrame(dict_list)
    df = df.drop("id", axis=1)
    df = df.drop("fraudulent", axis=1)
    test_X = preprocessing(df)

    dtest = xgb.DMatrix(data=test_X, enable_categorical=True)
    predicted = trained_model.predict(dtest)

    print("Completed.")
    return predicted