from sqlalchemy.orm import Session
from ..db import repository
from ..schemas.questionnaire import QuestionCreate, AnswerCreate

def get_next_question(db: Session, current_question_id: int, user_response: str):
    # Business logic to determine the next question
    # This can involve complex decision trees or logic
    
    # Example: Simply get the next question
    next_question_id = current_question_id + 1
    next_question = repository.get_question(db, next_question_id)
    return next_question

def create_question(db: Session, question: QuestionCreate):
    return repository.create_question(db, question.text, question.options)

def save_answer(db: Session, answer: AnswerCreate):
    return repository.save_answer(db, answer.question_id, answer.response)
