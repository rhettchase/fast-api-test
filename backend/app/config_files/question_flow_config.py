# Define a dictionary to map question IDs to next question logic based on response
from typing import Any, Union

# Rule-based system
# True acts as a catch-all for cases where specific conditions aren't met. This is useful for providing default messages or actions.

# Define rules as functions or lambdas
QUESTION_FLOW = {
    1: [
        {
            "condition": lambda response: response.lower() == "yes",
            "next": 2
        },
        {
            "condition": lambda response: response.lower() == "no",
            "message": "You're not eligible due to location"
        }
    ],
    2: [
        {
            "condition": lambda response: response == "18-24" or response == "25-34" or response == "35-44" or response == "45+",
            "next": 3
        },
        {
            "condition": lambda response: response == "Under 18",  # Default case for under 18
            "message": "You're not eligible due to age"
        }
    ],
    3: [  # Income-related question
        {
            "condition": lambda response: response == "Under $20,000" or response == "$20,000 - $50,000",
            "next": 4
        },
        {
            "condition": lambda response: response == "$50,000 - $100,000" or response == "$100,000+",
            "next": 4  # Assume next step should be question 4
        },
        {
            "condition": lambda response: True,  # Default case
            "message": "You're not eligible due to income criteria"
        }
    ],
    4: [
        {
            "condition": lambda response: response.lower() == "yes",
            "next": 5
        },
        {
            "condition": lambda response: response.lower() == "no",
            "next": 6
        },
        {
            "condition": lambda response: True,  # Default case for any other response
            "message": "You're not eligible due to program interest"
        }
    ],
    5: [
        {
            "condition": lambda response: True,  # No further questions
            "message": "Congratulations! You're eligible for the premium program."
        }
    ],
    6: [
        {
            "condition": lambda response: True,  # No further questions
            "message": "Thank you for your interest! Check out our standard program."
        }
    ]
}

def get_next_question_id(question_id: int, response: Any) -> Union[int, str]:
    """
    Evaluate the rules for a given question and response.

    :param question_id: Current question ID
    :param response: User's response to the question
    :return: Next question ID or a message if applicable
    """
    rules = QUESTION_FLOW.get(question_id, [])
    for rule in rules:
        if rule["condition"](response):
            if "next" in rule:
                return rule["next"]
            if "message" in rule:
                return {"message": rule["message"]}
    return {"message": "No valid rule found"}
