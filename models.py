from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from setup_database import Base


# 戦歴
class Record(Base):
    __tablename__ = "records"

    id = Column(String, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey('predictions.quiz_id'), index=True)
    user_answer = Column(String)
    username = Column(String, unique=True, index=True)
    created_at = Column(Integer)

    AI_answer = relationship("Prediction", back_populates="records")


# AIの予測結果
class Prediction(Base):
    __tablename__ = "predictions"
    quiz_id = Column(Integer, primary_key=True, index=True)
    predicted_as = Column(String)
    
    records = relationship("Record", back_populates="AI_answer")