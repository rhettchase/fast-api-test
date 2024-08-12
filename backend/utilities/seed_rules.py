import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from app.db.models import Rule, Base
from app.config import DATABASE_URL

# Create a new SQLAlchemy engine and session
engine = sa.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the rules to insert
rules = [
    # Rules for question 1
    {"question_id": 1, "condition": "response.lower() == 'yes'", "next_question_id": 2, "message": None},
    {"question_id": 1, "condition": "response.lower() == 'no'", "next_question_id": None, "message": "You're not eligible due to location"},
    
    # Rules for question 2
    {"question_id": 2, "condition": "response == '18-24' or response == '25-34' or response == '35-44' or response == '45+'", "next_question_id": 3, "message": None},
    {"question_id": 2, "condition": "response == 'Under 18'", "next_question_id": None, "message": "You're not eligible due to age"},
    
    # Rules for question 3 (Income question)
    {"question_id": 3, "condition": "response == 'Under $20,000'", "next_question_id": None, "message": "You're not eligible due to income"},
    {"question_id": 3, "condition": "response == '$20,000 - $50,000' or response == '$50,000 - $100,000' or response == '$100,000+'", "next_question_id": 4, "message": None},

    # Rules for question 4 (Premium program)
    {"question_id": 4, "condition": "response.lower() == 'yes'", "next_question_id": None, "message": "Congratulations! You're eligible for the program."},
    {"question_id": 4, "condition": "response.lower() == 'no'", "next_question_id": None, "message": "You're eligible for the premium program, here are some benefits..."},

    # Rules for question 5 (Favorite fruit)
    {"question_id": 5, "condition": "response.lower() == 'banana'", "next_question_id": 6, "message": None},
    {"question_id": 5, "condition": "response.lower() == 'apple'", "next_question_id": 7, "message": None},
    {"question_id": 5, "condition": "True", "next_question_id": None, "message": "You're not eligible due to fruit choice"},

    # Final eligibility questions
    {"question_id": 6, "condition": "True", "next_question_id": None, "message": "Congratulations! You're eligible for the program."},
    {"question_id": 7, "condition": "True", "next_question_id": None, "message": "Congratulations! You're eligible for the program."},
]

# Insert the rules into the database
for rule in rules:
    new_rule = Rule(
        question_id=rule["question_id"],
        condition=rule["condition"],
        next_question_id=rule["next_question_id"],
        message=rule["message"]
    )
    session.add(new_rule)

# Commit the transaction
session.commit()

# Close the session
session.close()

print("Database seeded successfully!")
