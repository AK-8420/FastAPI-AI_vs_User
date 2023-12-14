from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from setup_database import Base


# 戦歴
class Record(Base):
    __tablename__ = "records"

    result_id = Column(String, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('quizs.id', ondelete="CASCADE"), index=True)
    user_answer = Column(String)
    username = Column(String, index=True)
    created_at = Column(DateTime)

    Quiz = relationship("Quiz", back_populates="records", uselist=False)


# AIの予測結果
class Prediction(Base):
    __tablename__ = "predictions"
    quiz_id = Column(Integer, ForeignKey('quizs.id', ondelete="CASCADE"), primary_key=True, index=True)
    result = Column(Boolean)
    
    Quiz = relationship("Quiz", back_populates="prediction", uselist=False)


# 問題文データ
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

    records = relationship("Record", back_populates="Quiz", uselist=True)
    prediction = relationship("Prediction", back_populates="Quiz", uselist=False)