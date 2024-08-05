import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Union
from ...db.repository import get_question, create_question, save_answer, get_db, get_all_questions
from ...services.questionnaire_service import QuestionnaireService
from ...schemas.questionnaire import QuestionCreate, Question, AnswerCreate, Answer
from ...db.models import Question as DBQuestion
from app.config_files.question_flow_config import QUESTION_FLOW

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize the questionnaire service
questionnaire_service = QuestionnaireService()

@router.post("/questions/", response_model=Question)
async def create_question_api(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = create_question(db, question)
    return db_question

@router.get("/questions/{question_id}", response_model=Question)
async def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = get_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question  # Directly return if options is a list

@router.get("/questions/", response_model=List[Question])
async def list_questions(db: Session = Depends(get_db)):
    questions = get_all_questions(db)
    return questions

@router.post("/answers/", response_model=Answer)
async def create_answer_api(request: Request, answer: AnswerCreate, db: Session = Depends(get_db)):
    body = await request.json()
    logger.info(f"Raw request body: {body}")  # Log the raw request body
    logger.info(f"Received answer payload: question_id={answer.question_id} response={answer.response}")
    db_answer = save_answer(db, answer.question_id, answer.response)
    return db_answer

# @router.post("/next-question/", response_model=Union[Question, str])
# async def next_question(answer: AnswerCreate, db: Session = Depends(get_db)):
#     service = QuestionnaireService(QUESTION_FLOW)
#     next_question_id = service.get_next_question(answer.question_id, answer.response)

#     if isinstance(next_question_id, int):
#         next_question = get_question(db, next_question_id)
#         if not next_question:
#             raise HTTPException(status_code=404, detail="Next question not found")
#         return next_question

#     # Return a string if there are no more questions or an invalid response
#     return next_question_id  # Assuming next_question_id is already a string message

@router.post("/next-question/", response_model=Union[Question, dict])
async def next_question(answer: AnswerCreate, db: Session = Depends(get_db)):
    next_question_id = questionnaire_service.get_next_question(answer.question_id, answer.response)

    if isinstance(next_question_id, int):
        next_question = get_question(db, next_question_id)
        if not next_question:
            raise HTTPException(status_code=404, detail="Next question not found")
        return next_question

    # Return a string message directly if there are no further questions
    return next_question_id

@router.get("/form-config/{question_id}")
async def get_form_config(question_id: int, db: Session = Depends(get_db)):
    db_question = get_question(db, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Transform the question into a form schema
    form_config = {
        "title": "Dynamic Questionnaire",
        "fields": [
            {
                "name": f"question{db_question.id}",
                "type": "string",  # Assume text input; adjust type as necessary
                "label": db_question.text,
                "options": db_question.options  # assuming db_question.options is a list
            }
        ]
    }
    return form_config

