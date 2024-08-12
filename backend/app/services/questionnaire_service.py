import csv
from sqlalchemy.orm import Session
from ..db import repository
from ..schemas.questionnaire import QuestionCreate, AnswerCreate
from typing import Union, Any


class QuestionnaireService:
    def __init__(self, rules_file: str = 'data/questionnaire_rules.csv'):
        self.rules = self.load_rules_from_csv(rules_file)

    def load_rules_from_csv(self, rules_file: str) -> dict:
        """
        Load questionnaire rules from a CSV file.

        :param rules_file: Path to the CSV file containing the rules.
        :return: A dictionary mapping question IDs to their respective rules.
        """
        rules = {}
        with open(rules_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                question_id = int(row['question_id'])
                condition = row['condition'].strip()
                next_question_id = row['next_question_id'].strip() if row['next_question_id'] else None
                message = row['message'].strip() if row['message'] else None

                # Add rule to the dictionary
                if question_id not in rules:
                    rules[question_id] = []

                rules[question_id].append({
                    "condition": condition,
                    "next_question_id": int(next_question_id) if next_question_id else None,
                    "message": message
                })

        return rules

    def get_next_question(self, question_id: int, response: Any) -> Union[int, dict]:
        """
        Determine the next question based on the current question ID and response.

        :param question_id: Current question ID
        :param response: User's response to the question
        :return: Next question ID or a dictionary with a message
        """
        rules = self.rules.get(question_id, [])
        response = response.lower()  # Normalize response for matching

        for rule in rules:
            condition = rule["condition"].lower()
            if condition == response or condition == "true":
                if rule["next_question_id"]:
                    return rule["next_question_id"]
                if rule["message"]:
                    return {"message": rule["message"]}

        return {"message": "No valid rule found"}

def create_question(db: Session, question: QuestionCreate):
    return repository.create_question(db, question.text, question.options)

def save_answer(db: Session, answer: AnswerCreate):
    return repository.save_answer(db, answer.question_id, answer.response)
