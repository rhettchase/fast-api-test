from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from .models import Question, Answer, Rule
from ..schemas.questionnaire import QuestionCreate
from typing import List, Union, Dict

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()

def get_all_questions(db: Session):
    return db.query(Question).all()

def create_question(db: Session, question: QuestionCreate):
    db_question = Question(
        text=question.text,
        options=question.options
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def save_answer(db: Session, question_id: int, response: Union[str, List[str], Dict[str, Union[str, int, bool]]]) -> Answer:
    db_answer = Answer(question_id=question_id, response=response)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def create_rule(db: Session, rule_data: dict):
    rule = Rule(
        question_id=rule_data['question_id'],
        condition=rule_data['condition'],
        next_question_id=rule_data.get('next_question_id'),
        message=rule_data.get('message')
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

def get_rules_for_question(db: Session, question_id: int):
    return db.query(Rule).filter(Rule.question_id == question_id).all()
