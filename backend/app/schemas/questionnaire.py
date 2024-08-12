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
    response: Union[str, List[str], Dict[str, Union[str, int, bool]]]

    model_config = ConfigDict(from_attributes=True)

class AnswerCreate(BaseModel):
    question_id: int
    response: Union[str, List[str], Dict[str, Union[str, int, bool]]]

class Answer(AnswerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
# New RuleBase schema
class RuleBase(BaseModel):
    question_id: int
    condition: str
    next_question_id: Union[int, None] = None
    message: Union[str, None] = None

    model_config = ConfigDict(from_attributes=True)


# RuleCreate schema
class RuleCreate(RuleBase):
    pass

# Rule schema
class Rule(RuleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)