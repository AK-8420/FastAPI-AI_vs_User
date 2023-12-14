from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Record, Prediction, Quiz
import schemas

def get_record(db: Session, record_id: str):
    return db.query(Record).filter(Record.result_id == record_id).first()

def get_records_by_username(db: Session, username: str):
    return db.query(Record).filter(Record.username == username)

def get_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Record).offset(skip).limit(limit).all()

def create_record(db: Session, record_data: schemas.RecordCreate):
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
    return db.delete(instance)


def get_prediction(db: Session, prediction_id: int):
    return db.query(Prediction).filter(Prediction.quiz_id == prediction_id).first()

def create_prediction(db: Session, prediction_data: schemas.PredictionCreate):
    new_prediction = Prediction(**prediction_data.model_dump())
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction

def delete_prediction(db: Session, prediction_id: int):
    instance = get_prediction(db, prediction_id)
    return db.delete(instance)


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
    return db.delete(instance)