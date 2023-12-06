# 1時間でRESTful API実装チャレンジ
RESTful APIの基本的なメソッド（GET, POST, PUT/PATCH, DELETE）の実装練習

AIとユーザーで職務記述書が偽物かどうか予測し、その精度対決を行う。
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
    git clone ...
    ```
2. 仮想環境をactivate

    Windows PowerShellの場合
    ```terminal
    .\.venv\Scripts\Activate.ps1
    ```
3. SQLiteデータベースを作成
    ```
    python createDB.py
    ```
4. ローカルサーバーを立てる
    ```terminal
    uvicorn main:app --reload
    ```
5. [http://128.0.0.1/docs](http://128.0.0.1/)でアクセスポイントの確認

## 構成
- サーバープログラム（python）
  - FastAPI
  - uvicorn
  - SQLite
    - PostgreSQLも候補だったがサーバー複数にする予定はないのでこれで十分
- AI
  - scikit-learn
  - xgboost
    - 学習が早く、精度も良いらしいのでXGBoostを採用
  - データセット: [Real / Fake Job Posting Prediction](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction)

## チャレンジの軌跡