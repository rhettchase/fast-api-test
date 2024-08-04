from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...db.repository import get_question, create_question, save_answer, get_db, get_all_questions
from ...services.questionnaire_service import get_next_question
from ...schemas.questionnaire import QuestionCreate, Question, AnswerCreate, Answer
from ...db.models import Question as DBQuestion

router = APIRouter()

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
async def create_answer_api(answer: AnswerCreate, db: Session = Depends(get_db)):
    return save_answer(db, answer)

@router.post("/next-question/", response_model=Question)
async def next_question(answer: AnswerCreate, db: Session = Depends(get_db)):
    next_question = get_next_question(db, answer)
    if not next_question:
        raise HTTPException(status_code=404, detail="No further questions")
    return next_question
