""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the attendance including :

 1 -  The base attendance will output all attendance info including the user and manual entry 
        which will be crucial in displaying attendance records

 2 -  Attendance Create will just inherit all of the parent class info to create a new record
        
 3 -  Reading attendance , only the id is enough as i said before we dont want a lot fo api communication for speed

"""


from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttendanceSheetBase(BaseModel):
    user_id: int
    attendance_uid: Optional[str] = None
    attendance_date: Optional[datetime] = None
    logged_at: Optional[datetime] = None
    status: Optional[str] = None  # present / late / absent
    manual_entry: Optional[bool] = None
    session_tag: Optional[str] = None
    source: Optional[str] = None  # manual / scan

class AttendanceSheetCreate(AttendanceSheetBase):
    pass

class AttendanceSheetRead(AttendanceSheetBase):
    id: int

    class Config:
        from_attributes = True
