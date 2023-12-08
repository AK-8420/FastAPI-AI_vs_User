import time
import uuid
from pydantic import BaseModel, ConfigDict


class RecordBase(BaseModel):
    quiz_id: int
    user_answer: str
    username: str = "Unknown user"
    created_at: int = None

class RecordCreate(RecordBase):
    id: str = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid.uuid4())
        self.created_at = self.created_at or int(time.time())

class Record(RecordBase):
    id: str

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
