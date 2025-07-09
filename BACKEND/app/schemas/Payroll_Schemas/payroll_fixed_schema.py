""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is the schmea for history a design choice i made ot keep history seperated this schema will refelect 
appending only no updates


"""

from pydantic import BaseModel
from typing import Optional
from app.schemas.User_Schemas.user_schema import UserOut


class PayrollFixedBase(BaseModel):
    user_id: int
    base_salary: float


class PayrollFixedCreate(PayrollFixedBase):
    pass


class PayrollFixedUpdate(BaseModel):
    base_salary: float


class PayrollFixedRead(PayrollFixedBase):
    id: int
    total: float  
    



class PayrollFixedOut(PayrollFixedRead):
    user: Optional[UserOut]

    class Config:
        from_attributes = True
