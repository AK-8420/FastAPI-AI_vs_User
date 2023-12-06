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
2. 仮想環境をactivate

    Windows PowerShellの場合
    ```terminal
    .\.venv\Scripts\Activate.ps1
    ```
3. setup.pyで初期設定を実行
    ```
    python setup.py
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

## 1時間でどこまで実装できるかチャレンジ
2023/12/06 21:45からスタート

まずタスクの書き出しを行った (10分)
- setup.pyの作成
  - SQLite DBの作成
  - モデル学習
    - データセットの偽文800個のうち、80個をテストデータ、その他を訓練データとする
    - テストデータのみcsvファイルで保存
- main.pyの作成
  - 対決機能実装
    - 問題文の取得
    - ユーザー回答の送信
    - 結果の返答
  - 戦歴一覧機能実装
    - 現在の戦歴の取得
    - 特定の戦歴の削除
    - 特定の戦歴のユーザー名の修正

ＤＢのテーブル構成を考えた（3分）
- 戦歴テーブル
  - ハッシュID（String）
  - 日時（UNIX時間、Integer）
  - ユーザー名（String）
  - 勝敗（Integer）

SQLiteファイルの作成（9分）

問題文(ダミー)の取得を実装（12分、簡単な動作確認してから実装）

ユーザー回答の送信を実装（16分、クエリの扱いに手間取った）

結果(ダミー)の返答を実装（10分）

2023/12/06 22:45に終了。対決機能の枠組みだけ完成するという結果になった。

## 1時間実装していく中で思ったこと
- ユーザー回答の送信タイミングで回答の正否を評価するか、結果の表示タイミングで評価するか迷った
  - 結果の表示時の方がひとつの関数につきひとつの機能を備えるようになってよさそうと最終的に判断。
- 問題文（テストデータ）が固定なので、AIにはセットアップ時に事前に全問の回答を考えさせた方が処理時間の削減になるだろう
- Ruby on Railsみたいにテストを自動化したい