"""

Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - Submitting Sick Note (HR & Employee)
 - Reviewing Sick Note (HR)
 - Fetching current user Sick Notes
 - Fetching all Sick Notes


"""


from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from fastapi import UploadFile, Form , File

from typing import List
from datetime import datetime

from app.schemas.Attendance_Schemas.sick_notes_schema import SickNoteCreate, SickNoteRead
from app.controllers.Attendance_Controllers import sick_notes_controller
from app.core.dependencies import get_current_user , require_role
from app.database.session import get_db
from app.models.User_Models.user_model import User
from app.models.Attendance_Models.sick_note_model import SickNote 

router = APIRouter(prefix="/sick-notes", tags=["Sick Notes"])


# Submit sick note (Employee/HR)
@router.post("/submit")
async def submit_sick_note(
    attendance_id: int = Form(...),
    reason: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file_name = file.filename if file else None
    # Optional: Save file here if needed

    sick_note = SickNote(
        attendance_id=attendance_id,
        reason=reason,
        file_name=file_name,
        status="pending",
        submitted_at=datetime.now(),
        user_id=current_user.id
    )
    db.add(sick_note)
    db.commit()
    db.refresh(sick_note)
    return sick_note


# HR: Review sick note (approve/reject)
@router.put("/review/{note_id}", response_model=SickNoteRead,
            dependencies=[Depends(require_role(["hr", "admin"]))])
def review_note(note_id: int, decision: str = Query(...), comment: str = Query(""),
                reviewer=Depends(get_current_user), db: Session = Depends(get_db)):
    return sick_notes_controller.review_sick_note(note_id, decision, comment, reviewer, db)


# Get my sick notes (Employee/HR)
@router.get("/my/", response_model=List[SickNoteRead],
            dependencies=[Depends(require_role(["employee", "hr"]))])
def get_my_notes(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return sick_notes_controller.get_user_sick_notes(user.id, db)


# HR: View all sick notes
@router.get("/all", response_model=List[SickNoteRead],
            dependencies=[Depends(require_role(["hr"]))])
def get_all_notes(db: Session = Depends(get_db)):
    return sick_notes_controller.get_all_sick_notes(db)

@router.get("/user/{user_id}", response_model=List[SickNoteRead])
def get_sick_notes_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return sick_notes_controller.get_user_sick_notes(user_id, db)