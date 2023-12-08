from sqlalchemy.orm import Session
from models import Record, Prediction
import schemas

def get_record(db: Session, record_id: str):
    return db.query(Record).filter(Record.id == record_id).first()

def get_record_by_username(db: Session, username: str):
    return db.query(Record).filter(Record.username == username).first()

def get_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Record).offset(skip).limit(limit).all()

def create_record(db: Session, record_data: schemas.RecordCreate):
    new_record = Record(**record_data.model_dump())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def get_prediction(db: Session, prediction_id: int):
    return db.query(Prediction).filter(Prediction.quiz_id == prediction_id).first()

def get_predictions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Prediction).offset(skip).limit(limit).all()

def create_prediction(db: Session, prediction_data: schemas.PredictionCreate):
    new_prediction = Prediction(**prediction_data.model_dump())
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction