import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# 容量削減のためにintをboolに変換
def int2bool(value):
    if value == 0:
        return False
    else:
        return True

class RecordBase(BaseModel):
    result_id: str = None
    quiz_id: int
    user_answer: str
    username: str = "Unknown user"
    created_at: datetime = None

class RecordCreate(RecordBase):
    quiz_id: int
    user_answer: str
    username: str = "Unknown user"
    
    def __init__(self, **data):
        super().__init__(**data)
        self.result_id = str(uuid.uuid4())
        self.created_at = datetime.now()

class Record(RecordBase):
    result_id: str

    model_config = ConfigDict(
        from_attributes = True
    )


class PredictionBase(BaseModel):
    quiz_id: int # ズレ防止のためにid手動指定

class PredictionCreate(PredictionBase):
    predicted_as: int

    def __init__(self, **data):
        data["predicted_as"] = int2bool(data["predicted_as"])
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