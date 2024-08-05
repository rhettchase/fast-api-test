from pydantic import BaseModel, ConfigDict
from typing import List, Union, Dict

class QuestionBase(BaseModel):
    text: str
    options: List[str]

    model_config = ConfigDict(from_attributes=True)
    

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
        
class AnswerBase(BaseModel):
    question_id: int
    response: Union[List[str], Dict[str, Union[str, int, bool]]] 
    
    model_config = ConfigDict(from_attributes=True) 

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
