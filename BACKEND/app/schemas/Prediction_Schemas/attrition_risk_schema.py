""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the appraisals including :

 1 -  The base appraisals will output all appraisals info  

 2 -  Appraisals Create will just inherit all of the parent class info to create a new news post
        
 3 -  Reading Appraisala , only the id is enough as i said before we dont want a lot fo api communication for speed
"""

from pydantic import BaseModel ,Field
from typing import Optional
from datetime import datetime
from typing import Literal


class AttritionRiskInput(BaseModel):
    age: int
    gender: Literal['male', 'female', 'other']
    marital_status: Literal['single', 'married', 'divorced', 'widowed']
    months_at_company: int
    num_appraisals: int
    base_salary: float
    num_penalties: int
    num_raise_requests: int
    num_benefits: int
    past_performance_score: float
    sentiment_score: float
    attendance_rate: float
    completion_rate: float

class AttritionRiskOutput(BaseModel):
    attrition_class: Literal[0, 1, 2, 3]
    label: str = Field(..., description="Label such as 'Very Low Risk', 'Low Risk', etc.")


    class Config:
        from_attributes = True