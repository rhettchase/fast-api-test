from sqlalchemy.orm import Session
from ..db import repository
from ..schemas.questionnaire import QuestionCreate, AnswerCreate
from app.config_files.question_flow_config import get_next_question_id
from typing import Union, Any
from ..db.models import Rule
import logging

logger = logging.getLogger(__name__)

class QuestionnaireService:
    def __init__(self, db: Session):
        self.db = db

    def get_rules_for_question(self, question_id: int):
        return self.db.query(Rule).filter(Rule.question_id == question_id).all()

    def get_next_question(self, question_id: int, response: Any) -> Any:
        rules = self.get_rules_for_question(question_id)
        for rule in rules:
            if self.evaluate_condition(rule.condition, response):
                if rule.next_question_id is not None:
                    return rule.next_question_id
                if rule.message:
                    return {"message": rule.message}
        return {"message": "No valid rule found"}

    def evaluate_condition(self, condition: str, response: str) -> bool:
        try:
            local_scope = {"response": response}
            result = eval(condition, {}, local_scope)
            logger.info(f"Evaluating condition: {condition} with response: {response} => Result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error evaluating condition: {condition} with response: {response}. Error: {e}")
            return False



def create_question(db: Session, question: QuestionCreate):
    return repository.create_question(db, question.text, question.options)

def save_answer(db: Session, answer: AnswerCreate):
    return repository.save_answer(db, answer.question_id, answer.response)
