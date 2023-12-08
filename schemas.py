from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(
        from_attributes = True
    )


class PredictionBase(BaseModel):
    predicted_as: str

class PredictionCreate(PredictionBase):
    pass

class Prediction(PredictionBase):
    quiz_id: int

    model_config = ConfigDict(
        from_attributes = True
    )
