"""
Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - Pushing Attendance-Sheet to History
 - Fetch user hisotry by id 
 - Fetch all attendance histories



"""

from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.controllers.Attendance_Controllers import attendance_history_controller
from app.schemas.Attendance_Schemas.attendance_history_schema import AttendanceHistoryOut
from app.models.Attendance_Models.attendance_history_model import AttendanceHistory
from app.core.dependencies import get_current_user , require_role
from app.database.session import get_db

router = APIRouter(prefix="/attendance-history", tags=["Attendance History"])


# Push finalized sheet to history (Admin only)
@router.post("/push", dependencies=[Depends(require_role(["admin"]))])
def archive_session(db: Session = Depends(get_db)):
    return attendance_history_controller.push_attendance_to_history(db)


# Get my history (Employee/HR)
@router.get("/my", response_model=List[AttendanceHistoryOut],
            dependencies=[Depends(require_role(["employee", "hr"]))])
def get_my_history(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return attendance_history_controller.get_user_history(user.id, db)


# Get full history (Admin/HR)
@router.get("/all", response_model=List[AttendanceHistoryOut],
            dependencies=[Depends(require_role(["admin", "hr"]))])
def get_all_history(db: Session = Depends(get_db)):
    return attendance_history_controller.get_all_history(db)



@router.get("/by-id/{attendance_id}")
def get_attendance_by_id(attendance_id: int, db: Session = Depends(get_db)):
    record = db.query(AttendanceHistory).filter(AttendanceHistory.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance history record not found")
    return record

