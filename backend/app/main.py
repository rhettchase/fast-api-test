from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import questionnaire
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://192.168.68.61:3000"],  # Allows requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(questionnaire.router, prefix="/api/v1", tags=["questionnaire"])
