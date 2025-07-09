""""
Controllers are responsible for the application logic that is sent to routes and proccessed at request .

A future enhancement would be to implement services and seperate business logic but this is not necessary 
right now we dont have that many features so eveyrthing can be handled in controllers.

This File includes : 
 - Pushing Attendance-Sheet to History
 - Fetch user hisotry by id 
 - Fetch all attendance histories



"""


from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, datetime
from typing import List
from app.models.Attendance_Models.attendance_sheet_model import AttendanceSheet
from app.models.Attendance_Models.attendance_history_model import AttendanceHistory 
from app.schemas.Attendance_Schemas.attendance_history_schema import AttendanceHistoryOut


# Push all current sheet records to history table
def push_attendance_to_history(db: Session):
    sheet_records: List[AttendanceSheet] = db.query(AttendanceSheet).all()
    if not sheet_records:
        raise HTTPException(status_code=404, detail="No attendance sheet found.")

    for record in sheet_records:
        history = AttendanceHistory(
            attendance_id=record.id,
            user_id=record.user_id,
            date=record.attendance_date.date(),
            status=record.status if record.status else "absent",  # default to absent
        )
        db.add(history)

    db.commit()
    return {"message": f"{len(sheet_records)} records archived into attendance_history."}


# Get history for one user
def get_user_history(user_id: int, db: Session):
    return db.query(AttendanceHistory).filter(AttendanceHistory.user_id == user_id).all()


# Get all history (HR/Admin)
def get_all_history(db: Session):
    return db.query(AttendanceHistory).all()
