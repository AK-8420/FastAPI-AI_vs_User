from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from setup_database import Base


# 戦歴
class Record(Base):
    __tablename__ = "records"

    result_id = Column(String, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('predictions.quiz_id'), index=True)
    user_answer = Column(String)
    username = Column(String, index=True)
    created_at = Column(DateTime)

    AI_answer = relationship("Prediction", back_populates="records")


# AIの予測結果
class Prediction(Base):
    __tablename__ = "predictions"
    quiz_id = Column(Integer, primary_key=True, index=True)
    predicted_as = Column(Boolean)
    
    records = relationship("Record", back_populates="AI_answer")


# 問題文データ（サーバー再起動後も保存するため）
class Quiz(Base):
    __tablename__ = "quizs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    location = Column(String)
    department = Column(String)
    salary_range = Column(String)
    company_profile = Column(String)
    description = Column(String)
    requirements = Column(String)
    benefits = Column(String)
    telecommuting = Column(Boolean)
    has_company_logo = Column(Boolean)
    has_questions = Column(Boolean)
    employment_type = Column(String)
    required_experience = Column(String)
    required_education = Column(String)
    industry = Column(String)
    function = Column(String)
    fraudulent = Column(Boolean)