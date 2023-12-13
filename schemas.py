import time
import uuid
from pydantic import BaseModel, ConfigDict

# 容量削減のためにintをboolに変換
def int2bool(value):
    if value == 0:
        return False
    else:
        return True

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
    quiz_id: int # ズレ防止のためにid手動指定

class PredictionCreate(PredictionBase):
    predicted_as: int

    def __init__(self, **data):
        self.predicted_as = int2bool(self.predicted_as)
        super().__init__(**data)

class Prediction(PredictionBase):
    model_config = ConfigDict(
        from_attributes = True
    )


class QuizBase(BaseModel):
    title: str
    location: str
    department: str
    salary_range: str
    company_profile: str
    description: str
    requirements: str
    benefits: str
    telecommuting: bool
    has_company_logo: bool
    has_questions: bool
    employment_type: str
    required_experience: str
    required_education: str
    industry: str
    function: str


class QuizCreate(QuizBase):
    def __init__(self, **data):
        self.telecommuting = self.int2bool(self.telecommuting)
        self.has_company_logo = self.int2bool(self.has_company_logo)
        self.has_questions = self.int2bool(self.has_questions)
        self.fraudulent = self.int2bool(self.fraudulent)
        super().__init__(**data)


class Quiz(QuizBase):
    id: int

    model_config = ConfigDict(
        from_attributes = True
    )