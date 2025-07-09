from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import  Depends
from fastapi import HTTPException
from app.models.User_Models.user_model import User
from app.models.Training_and_Skills_Models.departments_model import Department
from app.models.Attendance_Models.attendance_history_model import AttendanceHistory
from app.models.Payroll_Models.appraisals_model import Appraisal
from app.models.Payroll_Models.penalty_model import Penalty
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from app.models.User_Models.performance_metrics_model import PerformanceMetric
from app.models.User_Models.personal_data_model import PersonalData
from app.models.Attendance_Models.attendance_history_model import AttendanceHistory
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed




def get_user_status(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    department = db.query(Department.name).filter(Department.id == user.department_id).scalar()
    salary = db.query(PayrollFixed.base_salary).filter(PayrollFixed.user_id == user_id).scalar()
    completion_rate = db.query(PerformanceMetric.completion_rate).filter(PerformanceMetric.user_id == user_id).scalar()
    marital_status = db.query(PersonalData.marital_status).filter(PersonalData.user_id == user_id).scalar()

    present_days = db.query(func.count()).select_from(AttendanceHistory).filter(AttendanceHistory.user_id == user_id, AttendanceHistory.status == "present").scalar()
    absent_days = db.query(func.count()).select_from(AttendanceHistory).filter(AttendanceHistory.user_id == user_id, AttendanceHistory.status == "absent").scalar()
    late_days = db.query(func.count()).select_from(AttendanceHistory).filter(AttendanceHistory.user_id == user_id, AttendanceHistory.status == "late").scalar()

    total_appraisals = db.query(func.sum(Appraisal.amount)).filter(Appraisal.user_id == user_id).scalar() or 0
    total_penalties = db.query(func.sum(Penalty.amount)).filter(Penalty.user_id == user_id).scalar() or 0

    return {
        "name": user.username,
        "department": department,
        "status": "Active",  # or pull from prediction table
        "task_completion_rate": completion_rate or 0,
        "attendance": {
            "present": present_days,
            "absent": absent_days,
            "late": late_days
        },
        "payroll": {
            "salary": salary or 0,
            "total_appraisals": total_appraisals,
            "total_penalties": total_penalties
        },
        "personal": {
            "marital_status": marital_status
        }
    }
