from sqlalchemy import func, case, and_
from sqlalchemy.orm import Session

from models import Record, Prediction, Quiz
import schemas
from schemas import str2bool

def get_record(db: Session, record_id: str):
    return db.query(Record).filter(Record.result_id == record_id).first()

def get_records_by_username(db: Session, username: str):
    return db.query(Record).filter(Record.username == username)

def get_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Record).offset(skip).limit(limit).all()

def create_record(db: Session, record_data: schemas.RecordCreate):
    quiz = db.query(Quiz).filter(Quiz.id == record_data.quiz_id).first()
    if quiz is None:
        raise ValueError(f"No Quiz found with id {record_data.quiz_id}")
    record_data.isCorrect = (str2bool(record_data.answer) == quiz.fraudulent)

    new_record = Record(**record_data.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def update_record(db: Session, record_id: str, username: str):
    instance = get_record(db, record_id)
    instance.username = username
    db.commit()
    return get_record(db, record_id) # 更新後のデータ

def delete_record(db: Session, record_id: str):
    instance = get_record(db, record_id)
    if instance:
        db.delete(instance)
        db.commit()
        return True
    else:
        return False

def get_records_accuracy(db: Session):
    # 各QuizごとにRecordの正しい予測の割合を計算 (RecordのないQuizは無視)
    query = db.query(
        Quiz.id,
        func.count(Record.quiz_id).label("total"),
        func.sum(
            case(
                ((Record.isCorrect), 1),
                else_=0
            )
        ).label("correct")
    ).join(Quiz, Quiz.id == Record.quiz_id).group_by(Quiz.id).having(func.count(Record.quiz_id) > 0)

    # クエリ実行
    results = query.all()

    # 各Quizごとの正解率を計算し、平均を求める
    if not results:
        total_accuracy = 0
    else:
        s = 0
        for result in results:
            s = s + (result.correct / result.total) if result.total != 0 else s
        total_accuracy = s / len(results)

    return total_accuracy


def get_prediction(db: Session, quiz_id: int):
    return db.query(Prediction).filter(Prediction.quiz_id == quiz_id).first()

def create_prediction(db: Session, prediction_data: schemas.PredictionCreate):
    quiz = db.query(Quiz).filter(Quiz.id == prediction_data.quiz_id).first()
    if quiz is None:
        raise ValueError(f"No Quiz found with id {prediction_data.quiz_id}")
    prediction_data.isCorrect = (prediction_data.answer == quiz.fraudulent)

    new_prediction = Prediction(**prediction_data.model_dump())
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction

def delete_prediction(db: Session, quiz_id: int):
    instance = get_prediction(db, quiz_id)
    if instance:
        db.delete(instance)
        db.commit()
        return True
    else:
        return False

def get_prediction_accuracy(db: Session):
    # PredictionとQuizをjoinし、正しい予測の数を集計するクエリ
    query = db.query(
        func.count(Prediction.quiz_id).label("total"),
        func.sum(case((Prediction.isCorrect, 1), else_=0)).label("correct")
    ).join(Quiz, Quiz.id == Prediction.quiz_id)

    # クエリ実行
    result = query.one()

    # 正しい予測の割合を計算
    if result.total == 0:
        return 0
    else:
        return result.correct / result.total


def get_quiz_count(db: Session):
    return db.query(func.count(Quiz.id)).scalar()

def get_quiz(db: Session, quiz_id: int):
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()

def get_quizs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Quiz).offset(skip).limit(limit).all()

def create_quiz(db: Session, quiz_data: schemas.QuizCreate):
    new_quiz = Quiz(**quiz_data.model_dump())
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz

def delete_quiz(db: Session, quiz_id: int):
    instance = get_quiz(db, quiz_id)
    if instance:
        db.delete(instance)
        db.commit()
        return True
    else:
        return False