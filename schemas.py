import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from sqlalchemy import orm

# 容量削減のためにintをboolに変換
def int2bool(value: int):
    if value == 0:
        return False
    else:
        return True

def str2bool(text: str):
    if text == "Real":
        return False
    else:
        return True


class RecordBase(BaseModel):
    result_id: str = "Not required"
    created_at: datetime = None
    quiz_id: int
    username: str = "Unknown user"
    user_answer: str = "Real or Fake"
    isCorrect: bool = None


class RecordCreate(RecordBase):
    def __init__(self, **data):
        super().__init__(**data)
        self.result_id = str(uuid.uuid4())
        self.created_at = datetime.now()

    @orm.reconstructor
    def on_load(self):
        self.isCorrect = (self.user_answer == self.Quiz.fraudulent)


class Record(RecordBase):
    result_id: str

    model_config = ConfigDict(
        from_attributes = True
    )


class PredictionBase(BaseModel):
    quiz_id: int # ズレ防止のためにid手動指定
    isCorrect: bool = None


class PredictionCreate(PredictionBase):
    answer: int

    def __init__(self, **data):
        data["answer"] = int2bool(data["answer"])
        super().__init__(**data)
    
    @orm.reconstructor
    def on_load(self):
        self.isCorrect = (self.answer == self.Quiz.fraudulent)


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
    fraudulent: bool


class QuizCreate(QuizBase):
    def __init__(self, **data):
        data["telecommuting"] = int2bool(data["telecommuting"])
        data["has_company_logo"] = int2bool(data["has_company_logo"])
        data["has_questions"] = int2bool(data["has_questions"])
        data["fraudulent"] = int2bool(data["fraudulent"])
        super().__init__(**data)


class Quiz(QuizBase):
    id: int

    model_config = ConfigDict(
        from_attributes = True
    )