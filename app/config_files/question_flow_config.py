# question_flow_config.py

# Define a dictionary to map question IDs to next question logic based on response
QUESTION_FLOW = {
    1: {  # Question ID 1: "Do you live in Georgia?"
        "Yes": 2,  # Next question ID 2
        "No": 2    # Same next question ID 2
    },
    2: {  # Question ID 2: "What is your favorite fruit?"
        "Banana": 4,  # Next question ID 4
        "Apple": 5,   # Next question ID 5
        "default": "You're not eligible"  # Default response for other answers
    }
    # Add additional questions and logic here
}
