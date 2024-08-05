from sqlalchemy.orm import Session
from ..db import repository
from ..schemas.questionnaire import QuestionCreate, AnswerCreate
from app.config_files.question_flow_config import get_next_question_id
from typing import Union, Any

class QuestionnaireService:
    def __init__(self):
        pass

    def get_next_question(self, question_id: int, response: Any) -> Any:
        """
        Determine the next question based on the current question ID and response.

        :param question_id: Current question ID
        :param response: User's response to the question
        :return: Next question ID or a message
        """
        next_question = get_next_question_id(question_id, response)
        
        if isinstance(next_question, dict) and "message" in next_question:
            return next_question
        
        return next_question
    
# class QuestionnaireService:
#     def __init__(self, question_flow: dict):
#         self.question_flow = question_flow

#     def get_next_question(self, current_question_id: int, response: str) -> Union[int, str]:
#         # Retrieve the mapping for the current question
#         question_mapping = self.question_flow.get(current_question_id, {})

#         # Determine the next step based on the response
#         if response in question_mapping:
#             return question_mapping[response]  # Return the next question ID or message
#         return question_mapping.get("default", "No further questions")

def create_question(db: Session, question: QuestionCreate):
    return repository.create_question(db, question.text, question.options)

def save_answer(db: Session, answer: AnswerCreate):
    return repository.save_answer(db, answer.question_id, answer.response)
