from pydantic import BaseModel
from typing import Optional


class RecordBase(BaseModel):
    id: str # インクリメンタルではなくデータ生成時に指定するためここに追加
    quiz_id: int
    user_answer: str
    username: str
    created_at: int

class RecordCreate(RecordBase):
    pass

class Record(RecordBase):
    class Config:
        orm_mode = True


class PredictionBase(BaseModel):
    predicted_as: str

class PredictionCreate(PredictionBase):
    pass

class Prediction(PredictionBase):
    quiz_id: int

    class Config:
        orm_mode = True
