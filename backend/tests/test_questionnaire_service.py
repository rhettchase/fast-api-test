import pytest
import sys
from app.services.questionnaire_service import QuestionnaireService
from app.config_files.question_flow_config import QUESTION_FLOW

print("PYTHONPATH:", sys.path)
print("Python executable:", sys.executable)

# Initialize the questionnaire service with the question flow configuration
service = QuestionnaireService(QUESTION_FLOW)

def test_next_question_for_georgia_resident():
    # Test scenario where the user lives in Georgia
    next_question_id = service.get_next_question(1, "Yes")
    assert next_question_id == 2, "Expected next question ID to be 2 for Georgia residents"

def test_next_question_for_favorite_fruit_banana():
    # Test scenario where the user selects "Banana" as their favorite fruit
    next_question_id = service.get_next_question(2, "Banana")
    assert next_question_id == 4, "Expected next question ID to be 4 for response 'Banana'"

def test_next_question_for_favorite_fruit_apple():
    # Test scenario where the user selects "Apple" as their favorite fruit
    next_question_id = service.get_next_question(2, "Apple")
    assert next_question_id == 5, "Expected next question ID to be 5 for response 'Apple'"

def test_ineligible_response():
    # Test scenario where the user selects an ineligible fruit
    result = service.get_next_question(2, "Orange")
    assert result == "You're not eligible", "Expected ineligible message for response 'Orange'"

def test_no_question_flow():
    # Test scenario where no further questions are available
    result = service.get_next_question(99, "Any response")
    assert result == "No further questions", "Expected no further questions for unknown question ID"
