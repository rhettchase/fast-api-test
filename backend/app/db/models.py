from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    options = Column(JSON)

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    response = Column(JSON)  # Response stored as JSON

    question = relationship("Question", back_populates="answers")

Question.answers = relationship("Answer", order_by=Answer.id, back_populates="question")

# Define the Rule model
class Rule(Base):
    __tablename__ = 'rules'
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, index=True)
    condition = Column(Text, nullable=False)
    next_question_id = Column(Integer, nullable=True)
    message = Column(String, nullable=True)
