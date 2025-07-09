""""
Controllers are responsible for the application logic that is sent to routes and proccessed at request .

A future enhancement would be to implement services and seperate business logic but this is not necessary 
right now we dont have that many features so eveyrthing can be handled in controllers.

This File includes : 
 - Submitting Sick Note (HR & Employee)
 - Reviewing Sick Note (HR)
 - Fetching current user Sick Notes
 - Fetching all Sick Notes


"""


from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
from typing import List

from app.models.Attendance_Models.sick_note_model import SickNote 
from app.schemas.Attendance_Schemas.sick_notes_schema import SickNoteCreate
from app.models.Attendance_Models.attendance_sheet_model import AttendanceSheet
from app.models.Attendance_Models.attendance_history_model import AttendanceHistory

# Employee/HR submits a sick note
def submit_sick_note(user_id: int, data: SickNoteCreate, db: Session):
    attendance_record = db.query(AttendanceSheet).filter(AttendanceSheet.id == data.attendance_id).first()
    if not attendance_record:
        raise HTTPException(status_code=404, detail="Attendance record not found.")

    # Prevent submitting for another user's attendance
    if attendance_record.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot submit a sick note for another user’s attendance."
        )
    sick_note = SickNote(
        attendance_id=data.attendance_id,
        reason=data.reason,
        file_name=data.file_name,
        status="pending",
        submitted_at=datetime.now(),
        user_id=user_id 
    )

    db.add(sick_note)
    db.commit()
    db.refresh(sick_note)
    return sick_note



# HR reviews and updates a sick note status
def review_sick_note(note_id: int, decision: str, comment: str, reviewer, db: Session):
    note = db.query(SickNote).filter(SickNote.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Sick note not found.")

    # ✅ Use AttendanceHistory instead of AttendanceSheet
    attendance = db.query(AttendanceHistory).filter(AttendanceHistory.id == note.attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=400, detail="Linked attendance history record not found.")

    # ✅ Check if HR is reviewing their own note
    if reviewer.role == "hr" and reviewer.id == attendance.user_id:
        raise HTTPException(
            status_code=403,
            detail="HR cannot review their own sick note. Escalate to Admin."
        )

    # ✅ Apply review decision
    note.status = decision
    note.review_comments = comment
    db.commit()

    return note




# Employee/HR: View personal sick notes
def get_user_sick_notes(user_id: int, db: Session):
    return db.query(SickNote).join(AttendanceSheet).filter(AttendanceSheet.user_id == user_id).all()


# HR: View all sick notes
def get_all_sick_notes(db: Session):
    return db.query(SickNote).all()


def get_user_sick_notes(user_id: int, db: Session):
    return db.query(SickNote).filter(SickNote.user_id == user_id).all()