""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the penalty including :

 1 -  The base news will output all penalty info linking it to payroll which we will use to add the penalty to payroll

 2 -  Just creating a new Penalty
        
 3 -  Reading Penalty , only the id is enough as i said before we dont want a lot of api communication for speed

"""

from pydantic import BaseModel
from typing import Optional

class PenaltyBase(BaseModel):
    payroll_id: int
    amount: Optional[float] = None
    reason: Optional[str] = None

class PenaltyCreate(PenaltyBase):
    pass

class PenaltyRead(PenaltyBase):
    id: int

    class Config:
        from_attributes = True
