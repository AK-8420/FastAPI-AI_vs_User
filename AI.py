# モデルの構築
def get_trained_model(train_X, train_y, test_X, test_y):
    print("Now learning...")
    # 学習
    # model = ...
    print("Completed.")
    return 1 # 仮

# 予測結果リストを返す（偽文書なら1、本物文書なら0）
def get_predictions(trained_model):
    print("Now getting predictions...")
    # 予測
    # predicted = model.predicted(test_X)
    import random
    predicted = [random.randint(0,1)]*100
    print("Completed.")
    return predicted