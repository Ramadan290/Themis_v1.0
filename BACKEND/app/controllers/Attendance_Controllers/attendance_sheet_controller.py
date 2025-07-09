""""
Controllers are responsible for the application logic that is sent to routes and proccessed at request .

A future enhancement would be to implement services and seperate business logic but this is not necessary 
right now we dont have that many features so eveyrthing can be handled in controllers.

This File includes : 
 - Generating Attendance Sheet (Manual{admin} or automatically geenrated)
 - Logging Attendance (Employee & HR)
 - get all Attendance-Sheet Records (HR & Admin)
 - Update Attendance Status{present ,absent,late} (HR)
 - clear Attendance - sheet or overwrite it (Manual{admin} or Automatically generated)


"""

from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from fastapi import HTTPException, status
from app.models.Attendance_Models.attendance_sheet_model import AttendanceSheet
from app.models.User_Models.user_model import User
from app.schemas.Attendance_Schemas.attendance_sheet_schema import AttendanceSheetCreate
from typing import List


# Generate the dynamic attendance sheet for a session
def generate_attendance_sheet(db: Session, session_tag: str):
    users: List[User] = db.query(User).all()

    # Optional: Clear the old sheet
    db.query(AttendanceSheet).delete()
    db.commit()

    for user in users:
        sheet = AttendanceSheet(
            user_id=user.id,
            attendance_uid=f"{user.id}-{uuid.uuid4().hex[:6]}",
            attendance_date=datetime.now(),
            session_tag=session_tag,
            status=None,
            manual_entry=False
        )
        db.add(sheet)
    db.commit()
    return {"message": f"Attendance sheet generated for {len(users)} users."}


# Log attendance (HR or Employee via QR or button)
def log_attendance(user_id: int, source: str, db: Session):
    record = db.query(AttendanceSheet).filter(AttendanceSheet.user_id == user_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Attendance entry not found.")
    if record.status:
        raise HTTPException(status_code=400, detail="Attendance already logged.")

    record.status = "present"
    record.logged_at = datetime.now()
    record.source = source
    db.commit()
    return record


# Get all current attendance sheet records
def get_all_attendance(db: Session):
    return db.query(AttendanceSheet).all()


# Update a user's attendance status manually (Admin/HR)
def update_attendance_status(attendance_id: int, new_status: str, db: Session):
    record = db.query(AttendanceSheet).filter(AttendanceSheet.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found.")
    record.status = new_status
    record.manual_entry = True
    db.commit()
    return record


# Clear current sheet manually (For Testing purposes only)
def clear_attendance_sheet(db: Session):
    db.query(AttendanceSheet).delete()
    db.commit()
    return {"message": "Attendance sheet cleared."}
