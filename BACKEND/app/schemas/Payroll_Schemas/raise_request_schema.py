""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the raise-requests including :
 1 -  Submitting a raise-requests will output all the data including {payroll link} in which it will be used to 
        update payroll

 2 -  Creating a new raise-requests will jsut inherit everything from its parent class and 
        create a new request hence the optional columns
        
 3 -  Reading requests which will just return the request list , the id is enough to trigger all information 
        lets not load anything else onto the api we want minimal communication for speed

"""


from pydantic import BaseModel , validator
from typing import Optional
from datetime import datetime
from app.core.utils import format_datetime

from decimal import Decimal

class RaiseRequestBase(BaseModel):
    user_id: Optional[int]  # ✅ Make it optional
    requested_amount: Optional[float] = None
    reason: Optional[str] = None
    status: Optional[str] = None  # e.g., "pending", "approved"
    requested_at: Optional[str] = None  # <- change to str!

    @validator("requested_at", pre=True)
    def format_requested_at(cls, value):
        if isinstance(value, datetime):
            return format_datetime(value)
        return value

class RaiseRequestCreate(RaiseRequestBase):
    pass # inherit all
    # UID will be generated in the controller


class RaiseRequestReview(BaseModel):
    request_id: int
    status: str  # Must be "approved" or "rejected"
    review_comment: Optional[str] = None


class RaiseRequestRead(RaiseRequestBase):
    id: int
    request_uid: str
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[str] = None
    review_comment: Optional[str] = None

    @validator("reviewed_at", pre=True)
    def format_reviewed_at(cls, value):
        if isinstance(value, datetime):
            return format_datetime(value)
        return value

    class Config:
        from_attributes = True
