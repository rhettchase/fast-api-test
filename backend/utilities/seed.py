from app.db.repository import get_db
from app.db.models import Question
from sqlalchemy.orm import Session
from sqlalchemy import text

def reset_id_sequence(db: Session, table_name: str):
    """
    Reset the ID sequence of a given table in PostgreSQL.
    """
    db.execute(text(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1"))

def seed_database(db: Session):
    # Clear existing answers and questions
    db.execute(text("DELETE FROM answers"))
    db.execute(text("DELETE FROM questions"))
    db.commit()

    # Reset the ID sequence for the 'questions' table
    reset_id_sequence(db, "questions")

    # Add new questions
    questions = [
        Question(text="Do you live in California?", options=["Yes", "No"]),
        Question(text="How old are you?", options=["Under 18", "18-24", "25-34", "35-44", "45+"]),
        Question(text="What is your annual income?", options=["Under $20,000", "$20,000 - $50,000", "$50,000 - $100,000", "$100,000+"]),
        Question(text="Are you interested in our premium program?", options=["Yes", "No"]),
        Question(text="What is your favorite fruit?", options=["Apple", "Banana", "Orange", "Grape"]),
    ]

    for question in questions:
        db.add(question)

    db.commit()

if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))
    from app.db.repository import get_db

    db = next(get_db())
    seed_database(db)
