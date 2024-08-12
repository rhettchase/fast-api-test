import csv
from sqlalchemy.orm import Session
from ..db import repository
from ..schemas.questionnaire import QuestionCreate, AnswerCreate
from typing import Union, Any
import logging

logger = logging.getLogger(__name__)

class QuestionnaireService:
    def __init__(self, rules_file: str = 'data/questionnaire_rules.csv'):
        self.rules = self.load_rules_from_csv(rules_file)

    def load_rules_from_csv(self, rules_file: str) -> dict:
        """
        Load questionnaire rules from a CSV file.
        """
        rules = {}
        with open(rules_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                question_id = int(row['question_id'])
                condition = row['condition'].strip().lower()
                next_question_id = row['next_question_id'].strip() if row['next_question_id'] else None
                message = row['message'].strip() if row['message'] else None

                if next_question_id and next_question_id.isdigit():
                    next_question_id = int(next_question_id)

                if question_id not in rules:
                    rules[question_id] = []

                rules[question_id].append({
                    "condition": condition,
                    "next_question_id": next_question_id,
                    "message": message
                })

        return rules

    def evaluate_condition(self, condition: str, response: str) -> bool:
        """
        Safely evaluate a condition string with the given response.
        """
        response = response.lower()
        if condition == "true":
            return True
        return condition == response

    def get_next_question(self, question_id: int, response: Any) -> Any:
        """
        Determine the next question based on the current question ID and response.
        """
        rules = self.rules.get(question_id, [])
        response = response.lower()

        for rule in rules:
            if self.evaluate_condition(rule["condition"], response):
                if rule["next_question_id"] is not None:
                    return rule["next_question_id"]
                if rule["message"]:
                    return {"message": rule["message"]}

        return {"message": "No valid rule found"}

def create_question(db: Session, question: QuestionCreate):
    return repository.create_question(db, question.text, question.options)

def save_answer(db: Session, answer: AnswerCreate):
    return repository.save_answer(db, answer.question_id, answer.response)
