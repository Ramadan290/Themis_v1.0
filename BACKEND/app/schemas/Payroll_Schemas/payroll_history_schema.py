""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is the schmea for history a design choice i made ot keep history seperated this schema will refelect 
appending only no updates


"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.User_Schemas.user_schema import UserOut


class PayrollHistoryBase(BaseModel):
    user_id: int
    final_salary: float
    period: str
    status: Optional[str] = "processed"


class PayrollHistoryCreate(PayrollHistoryBase):
    pass


class PayrollHistoryRead(PayrollHistoryBase):
    id: int
    recorded_at: datetime
    total: float  # ✅ Show in responses



class PayrollHistoryOut(PayrollHistoryRead):
    user: Optional[UserOut]

    model_config = {
        "from_attributes": True
    }
