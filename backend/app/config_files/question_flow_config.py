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
            "next": 2
        }
    ],
    2: [
        {
            "condition": lambda response: response.lower() == "banana",
            "next": 4
        },
        {
            "condition": lambda response: response.lower() == "apple",
            "next": 5
        },
        {
            "condition": lambda response: True,  # Default case for any other response
            "message": "You're not eligible"
        }
    ],
    4: [
        {
            "condition": lambda response: True,  # No further questions
            "message": "No further questions"
        }
    ],
    5: [
        {
            "condition": lambda response: True,  # No further questions
            "message": "No further questions"
        }
    ]
}

def get_next_question_id(question_id: int, response: Any) -> Union[int, str]:
    rules = QUESTION_FLOW.get(question_id, [])
    for rule in rules:
        if rule["condition"](response):
            return rule.get("next") or rule.get("message", "No further questions")
    return "No further questions"


# QUESTION_FLOW = {
#     1: {  # Question ID 1: "Do you live in Georgia?"
#         "Yes": 2,  # Next question ID 2
#         "No": 2    # Same next question ID 2
#     },
#     2: {  # Question ID 2: "What is your favorite fruit?"
#         "Banana": 4,  # Next question ID 4
#         "Apple": 5,   # Next question ID 5
#         "default": "You're not eligible"  # Default response for other answers
#     }
#     # Add additional questions and logic here
# }
