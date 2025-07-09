""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the payroll including :

 1 -  Base Class will display user and his salary , no info needed for me to explain here i am not that dumb

 2 -  Creating a new Payroll just inherits eveyrhting as we are adding a new record
        
 3 -  Payroll Read , only the id is enough as i said before we dont want a lot fo api communication for speed 

 4 - Payroll Out , is a an approach i may take not sure but maybe to tie the user to his payroll directly i 
    feel its better to link them instead of calling both each time u know always think about performance even if we are not going to achieve it lmao anyways

"""
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from app.schemas.User_Schemas.user_schema import UserOut


class PayrollBase(BaseModel):
    user_id: int
    salary: Optional[float] = None
    status: Optional[Literal["draft", "approved", "processed"]] = "draft"


class PayrollCreate(PayrollBase):
    pass


class PayrollRead(PayrollBase):
    id: int
    created_at: datetime
    last_updated: datetime
    total: float  # ✅ Show in responses


class PayrollUpdate(BaseModel):
    salary: Optional[float] = None
    status: Optional[str] = None

class PayrollOut(PayrollRead):
    user: UserOut

    class Config:
        from_attributes = True
