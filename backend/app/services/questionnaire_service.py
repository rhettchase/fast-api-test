from sqlalchemy.orm import Session
from ..db import repository
from ..schemas.questionnaire import QuestionCreate, AnswerCreate
from app.config_files.question_flow_config import QUESTION_FLOW
from typing import Union

class QuestionnaireService:
    def __init__(self, question_flow: dict):
        self.question_flow = question_flow

    def get_next_question(self, current_question_id: int, response: str) -> Union[int, str]:
        # Retrieve the mapping for the current question
        question_mapping = self.question_flow.get(current_question_id, {})

        # Determine the next step based on the response
        if response in question_mapping:
            return question_mapping[response]  # Return the next question ID or message
        return question_mapping.get("default", "No further questions")

def create_question(db: Session, question: QuestionCreate):
    return repository.create_question(db, question.text, question.options)

def save_answer(db: Session, answer: AnswerCreate):
    return repository.save_answer(db, answer.question_id, answer.response)
