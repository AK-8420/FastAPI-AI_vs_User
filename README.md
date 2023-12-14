# あなたはAIよりうまく偽文書を見分けられるか？API
RESTful APIの基本的なメソッド（GET, POST, PUT/PATCH, DELETE）の実装練習

与えられた職務記述書に対し、AIとユーザーがそれぞれ偽文書かどうか判断する。そして、その精度を競う。
- 対決機能
  - GET: 問題文とIDの取得。
  - POST: ユーザーの回答の送信。
- みんなの戦歴一覧機能
  - GET: 戦歴一覧を取得。
  - PUT/PATCH: 戦歴上のユーザー名の変更。
  - DELETE: 戦歴を削除。

## 導入方法
ターミナルで以下のコードを実行する
1. リポジトリからデータをダウンロード
    ```terminal
    git clone git@github.com:AK-8420/FastAPI-AI_vs_User.git
    ```
2. 仮想環境を有効化

    Windows PowerShellの場合
    ```terminal
    cd FastAPI-AI_vs_User
    .\.venv\Scripts\Activate.ps1
    ```
3. setup.pyで初期設定を実行
    ```
    python setup.py
    ```
4. ローカルサーバーを立てる
    ```python
    python -m uvicorn main:app --reload
    ```
5. [http://128.0.0.1/docs](http://128.0.0.1/)でアクセスポイントの確認

## 遊び方
1. [http://128.0.0.1/quiz](http://128.0.0.1/quiz)にアクセスしてランダムに問題文を取得する
```
{
  "quiz_id": 3(例),
  "quiz": {
    ...問題文のデータ...
  }
}
```
2. [http://128.0.0.1/quiz](http://128.0.0.1/quiz)に問題文のID（quiz_id）と答えをPostする
```
{
  "quiz_id": 3,
  "user_answer": "Real"または"Fake",
  "username": "ユーザー名"（省略可能）
}
```
3. 結果IDが返ってくるので、[http://128.0.0.1/result/結果ID]()にアクセス
```
{
  "result_id": "1b4442e2-a880-402f-9dfe-174455921701", (結果ID)
  "quiz_id": 3,
  "user_answer": 先ほどの解答,
  "username": "ユーザー名",
  "created_at": "2023-12-14T20:27:09.976484"
}
```
4. AIの予測した回答と、AIとユーザーどちらが正しかったのかが確認できる
```
{
  "result_battle": "Win",
  "user_answer": "Real",
  "AI_answer": "Fake",
  "correct_answer": "Real"
}
```

## 構成
- サーバープログラム（python）
  - FastAPI
  - uvicorn
  - SQLite
    - PostgreSQLも候補だったがサーバー複数にする予定はないのでこれで十分
  - SQLAlchemy
    - 接続プール管理をしてくれる
- AI
  - scikit-learn
  - xgboost
    - 学習が早く、精度も良いらしいのでXGBoostを採用
  - データセット: [Real / Fake Job Posting Prediction](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction)