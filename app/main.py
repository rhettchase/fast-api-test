from fastapi import FastAPI
from .api.v1 import questionnaire

app = FastAPI()

app.include_router(questionnaire.router, prefix="/api/v1", tags=["questionnaire"])
