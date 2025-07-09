from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.Training_and_Skills_Models.departments_model import Department
from app.models.User_Models.user_model import User
from app.models.Payroll_Models.payroll_model import Payroll
from app.controllers.Users_Controllers.user_status_controller import get_user_status
from app.core.dependencies import get_db
from app.models.Payroll_Models.raise_request_model import RaiseRequest
from app.models.Training_and_Skills_Models.user_training_model import UserTraining
from app.models.User_Models.sentiment_inputs_model import SentimentInput
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from app.models.User_Models.performance_metrics_model import PerformanceMetric
from app.models.Attendance_Models.attendance_history_model import AttendanceHistory



router = APIRouter(prefix="/status", tags=["User Status"])

@router.get("/{user_id}")
def get_status(user_id: int, db: Session = Depends(get_db)):
    return get_user_status(user_id, db)






@router.get("/hr/analytics")
def get_hr_analytics(db: Session = Depends(get_db)):
    # 1. Attendance Summary (count by status)
    attendance_query = (
        db.query(AttendanceHistory.status, func.count().label("count"))
        .group_by(AttendanceHistory.status)
        .all()
    )
    attendance_summary = {status: count for status, count in attendance_query}

    # 2. Payroll Distribution (count by salary range, e.g. buckets)
    payrolls = db.query(Payroll.salary).all()
    payroll_distribution = {"3000-6000":0, "6000-9000":0, "9000-12000":0, "12000+":0}
    for (salary,) in payrolls:
        if salary <= 5000:
            payroll_distribution["3000-6000"] += 1
        elif salary <= 8000:
            payroll_distribution["6000-9000"] += 1
        elif salary <= 12000:
            payroll_distribution["9000-12000"] += 1
        else:
            payroll_distribution["12000+"] += 1

    # 3. Employee Distribution (count by department)
    emp_dist_query = (
        db.query(Department.name, func.count(User.id))
        .join(User, User.department_id == Department.id)
        .group_by(Department.name)
        .all()
    )
    employee_distribution = {name: count for name, count in emp_dist_query}

    # 4. Task Completion Distribution (from PerformanceMetrics.completion_rate)
    completion_query = db.query(PerformanceMetric.completion_rate).all()
    completion_distribution = {"0-50%":0, "60-70%":0, "80-100%":0}
    for (rate,) in completion_query:
        if rate <= 0.5:
            completion_distribution["0-50%"] += 1
        elif rate <= 0.8:
            completion_distribution["60-70%"] += 1
        else:
            completion_distribution["80-100%"] += 1

    # 5. Workload Distribution (example based on UserTraining progress)
    workload_query = db.query(UserTraining.progress).all()
    workload_distribution = {"Low":0, "Medium":0, "High":0}
    for (progress,) in workload_query:
        if progress <= 0.33:
            workload_distribution["Low"] += 1
        elif progress <= 0.66:
            workload_distribution["Medium"] += 1
        else:
            workload_distribution["High"] += 1

    # 6. Workload Balancing (simple example: count balanced vs unbalanced)
    # You might want to implement your own logic here
    workload_balancing = {"Balanced": 50, "Unbalanced": 50}  # Placeholder

    # 7. Raise Requests Summary (count by status)
    raise_query = (
        db.query(RaiseRequest.status, func.count())
        .group_by(RaiseRequest.status)
        .all()
    )
    raise_requests_summary = {status: count for status, count in raise_query}

    # 8. Interaction Summary (from SentimentInputs)
    # Summarize meetings, break_time, etc. Example counts or sums
    interaction_summary = {}
    meetings = db.query(func.sum(SentimentInput.meetings_attended)).scalar() or 0
    breaks = db.query(func.sum(SentimentInput.break_time)).scalar() or 0
    interaction_summary["Meetings"] = meetings
    interaction_summary["Break Time (hrs)"] = breaks

    return {
        "attendance_summary": attendance_summary,
        "payroll_distribution": payroll_distribution,
        "employee_distribution": employee_distribution,
        "task_completion_distribution": completion_distribution,
        "workload_distribution": workload_distribution,
        "workload_balancing": workload_balancing,
        "raise_requests_summary": raise_requests_summary,
        "interaction_summary": interaction_summary,
    }