""""

The schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is the schmea for history a design choice i made ot keep history seperated this schema will refelect 
appending only no updates

"""

from pydantic import BaseModel
from datetime import date, datetime

class AttendanceHistoryBase(BaseModel):
    attendance_id: int
    user_id: int
    date: date
    status: str  # present / late / absent / sick_leave

class AttendanceHistoryCreate(AttendanceHistoryBase):
    pass

class AttendanceHistoryOut(AttendanceHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
