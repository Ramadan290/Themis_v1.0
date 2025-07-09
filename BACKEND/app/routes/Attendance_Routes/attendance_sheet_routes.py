"""
Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - Generating Attendance Sheet (Manual{admin} or automatically geenrated)
 - Logging Attendance (Employee & HR)
 - get all Attendance-Sheet Records (HR & Admin)
 - Update Attendance Status{present ,absent,late} (HR)
 - clear Attendance - sheet or overwrite it (Manual{admin} or Automatically generated)



"""

from fastapi import APIRouter, Depends, status, Query , HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.Attendance_Schemas.attendance_sheet_schema import AttendanceSheetRead
from app.models.Attendance_Models.attendance_sheet_model import AttendanceSheet

from app.controllers.Attendance_Controllers import attendance_sheet_controller
from app.core.dependencies import get_current_user , require_role
from app.database.session import get_db

router = APIRouter(prefix="/attendance-sheet", tags=["Attendance Sheet"])


# Generate new sheet (Admin only)
@router.post("/generate", dependencies=[Depends(require_role(["admin"]))])
def generate_sheet(session_tag: str = Query(...), db: Session = Depends(get_db)):
    return attendance_sheet_controller.generate_attendance_sheet(db, session_tag)


# Employee logs attendance (HR & Employee)
@router.post("/log", response_model=AttendanceSheetRead,
             dependencies=[Depends(require_role(["employee", "hr"]))])
def log(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return attendance_sheet_controller.log_attendance(user.id, source="scan", db=db)


# HR/Admin view current sheet
@router.get("/all", response_model=List[AttendanceSheetRead],
            dependencies=[Depends(require_role(["hr", "admin"]))])
def get_sheet(db: Session = Depends(get_db)):
    return attendance_sheet_controller.get_all_attendance(db)


# HR/Admin update status manually
@router.put("/update/{attendance_id}", response_model=AttendanceSheetRead,
            dependencies=[Depends(require_role(["hr", "admin"]))])
def update_status(attendance_id: int, new_status: str = Query(...), db: Session = Depends(get_db)):
    return attendance_sheet_controller.update_attendance_status(attendance_id, new_status, db)


# Optional: Clear current session sheet
@router.delete("/clear", dependencies=[Depends(require_role(["admin"]))])
def clear_sheet(db: Session = Depends(get_db)):
    return attendance_sheet_controller.clear_attendance_sheet(db)
