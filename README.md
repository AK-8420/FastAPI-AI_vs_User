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
2. 仮想環境に入る

    Windows PowerShellの場合
    ```terminal
    cd FastAPI-AI_vs_User
    .\.venv\Scripts\Activate.ps1
    ```
3. ローカルサーバーを立てる
    ```python
    python -m uvicorn main:app --reload
    ```
4. [http://128.0.0.1/docs](http://128.0.0.1/)からAPIのエンドポイントを確認する。

### 備考
このAPIは約18000問あるデータからランダムに100問を選び、残りのデータをAIに学習させた後に出題する。

他の問題を遊びたい場合は、以下の手順に従う。
1. 学習済みモデル（tree_model.json）と古いデータ（history.db）を削除し、サーバーを再起動する。

2. "モデルを新しく生成しますか？"という旨の質問が出るので、```Y```(はい)と答える

3. データの前処理（embedding）、学習、予測が終わるまで待つ（1時間半ほど）
4. [http://128.0.0.1/docs](http://128.0.0.1/)にアクセスして遊ぶ

## 遊び方
1. [http://128.0.0.1/quiz](http://128.0.0.1/quiz)にGETリクエストを送り、ランダムに問題文を取得する
```
{
  "quiz_id": 3(例),
  "quiz": {
    ...問題文のデータ...
  }
}
```
2. [http://128.0.0.1/quiz](http://128.0.0.1/quiz)に問題文のID（quiz_id）とあなたの答えをPOSTする
```
{
  "quiz_id": 3,
  "answer": "Real"または"Fake",
  "username": "ユーザー名"（省略可能）
}
```
3. 以下のように結果IDが返ってくるので、[http://128.0.0.1/result/結果ID]()にGETリクエストを送る
  ```
  {
    "result_id": "1b4442e2-a880-402f-9dfe-174455921701", (結果ID)
    "created_at": "2023-12-14T20:27:09.976484"
  }
  ```
  するとAIの予測した回答と、正しい答えが確認できる
  ```
  {
    "Battle_result": "Win",
    "User_answer": "Real",
    "AI_answer": "Fake",
    "correct_answer": "Real"
  }
  ```
4. [http://128.0.0.1/result](http://128.0.0.1/result)でみんなの戦歴が確認可能
5. [http://128.0.0.1](http://128.0.0.1)でAIの正答率と、ユーザーの正答率の平均が確認できる。果たして人間たちはAIに勝てるか！？

## 構成
- サーバープログラム（python）
  - FastAPI
  - uvicorn
  - SQLite
    - PostgreSQLも候補だったがサーバー複数にする予定はないのでこれで十分
  - SQLAlchemy
    - 接続プール管理をしてくれる
- AI
  - xgboost
    - 学習が早く、空値も含むマルチインプットに適性があるのでXGBoostを採用
  - データセット: [Real / Fake Job Posting Prediction](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction)

## 制作記録
考えたことや試行錯誤したことのメモ
https://github.com/AK-8420/FastAPI-AI_vs_User/wiki