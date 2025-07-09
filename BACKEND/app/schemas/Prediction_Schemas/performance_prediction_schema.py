""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the appraisals including :

 1 -  The base appraisals will output all appraisals info  

 2 -  Appraisals Create will just inherit all of the parent class info to create a new news post
        
 3 -  Reading Appraisala , only the id is enough as i said before we dont want a lot fo api communication for speed
"""

from pydantic import BaseModel , Field
from typing import Literal
from datetime import datetime


class PerformancePredictionInput(BaseModel):
    attendance_rate: float
    num_penalties: int
    num_raise_requests: int
    appraisal_amount: float
    num_sick_notes: int
    benefits: int
    months_at_company: int
    completion_rate: float
    sentiment_score: int

class PerformancePredictionOutput(BaseModel):
    attrition_class: Literal[0, 1, 2, 3]
    label: str = Field(..., description="Label indicating performance" )

    class Config:
        from_attributes = True