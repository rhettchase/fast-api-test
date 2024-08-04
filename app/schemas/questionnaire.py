from pydantic import BaseModel
from typing import List, Union, Dict

class QuestionBase(BaseModel):
    text: str
    options: List[str]
    

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True
        
class AnswerBase(BaseModel):
    question_id: int
    response: Union[List[str], Dict[str, Union[str, int, bool]]] 

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int

    class Config:
        orm_mode = True
