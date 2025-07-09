""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the appraisals including :

 1 -  The base appraisals will output all appraisals info  

 2 -  Appraisals Create will just inherit all of the parent class info to create a new news post
        
 3 -  Reading Appraisala , only the id is enough as i said before we dont want a lot fo api communication for speed
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppraisalBase(BaseModel):
    payroll_id: int
    amount: Optional[float] = None
    appraisal_date: Optional[datetime] = None

class AppraisalCreate(AppraisalBase):
    pass

class AppraisalRead(AppraisalBase):
    id: int

    class Config:
        from_attributes = True
