""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the sick-notes including :

 1 -  Base class will just output everything in table for display and verification and 
       also put requests to update status later

 2 -  the create will just create a new sick note record hence why inherits eveyrhting from parent class
        
 3 -  Reading sick notes , only the id is enough as i said before we dont want a lot fo api communication for speed

"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SickNoteBase(BaseModel):
    attendance_id: int
    reason: Optional[str] = None
    status: Optional[str] = None  # pending, approved, rejected
    review_comments: Optional[str] = None
    file_name: Optional[str] = None
    submitted_at: Optional[datetime] = None

class SickNoteCreate(SickNoteBase):
    pass

class SickNoteRead(SickNoteBase):
    id: int

    class Config:
        from_attributes = True

