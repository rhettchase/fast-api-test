from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
from .models import Question, Answer
from ..schemas.questionnaire import QuestionCreate

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
    questions = db.query(Question).all()
    for question in questions:
        print(f"Question ID: {question.id}, Options: {question.options}, Type: {type(question.options)}")
    return questions

def create_question(db: Session, question: QuestionCreate):
    db_question = Question(
        text=question.text,
        options=question.options  # Pass options directly as a list
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def save_answer(db: Session, question_id: int, response: str):
    db_answer = Answer(question_id=question_id, response=response)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer
