""""
Controllers are responsible for the application logic that is sent to routes and proccessed at request .

A future enhancement would be to implement services and seperate business logic but this is not necessary 
right now we dont have that many features so eveyrthing can be handled in controllers.

This File includes : 



"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.Payroll_Models.payroll_model import Payroll
from app.models.Payroll_Models.payroll_history_model import PayrollHistory
from app.schemas.Payroll_Schemas.payroll_history_schema import PayrollHistoryCreate
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

def process_payroll_to_history(db: Session):
    from app.models.Payroll_Models.payroll_model import Payroll
    from app.models.Payroll_Models.payroll_history_model import PayrollHistory

    payrolls = db.query(Payroll).all()
    if not payrolls:
        raise HTTPException(status_code=400, detail="No payrolls found to archive.")

    count = 0
    archived_users = set()

    for record in payrolls:
        period = record.created_at.strftime("%Y-%m")  # ⬅️ extract actual period from each record

        key = (record.user_id, period)
        already_in_db = db.query(PayrollHistory).filter_by(user_id=record.user_id, period=period).first()

        if already_in_db or key in archived_users:
            continue

        db.add(PayrollHistory(
            user_id=record.user_id,
            final_salary=record.salary,
            period=period,
            status="processed",
            recorded_at=datetime.utcnow(),
            total=record.total
        ))
        archived_users.add(key)
        count += 1

    db.commit()

    if count == 0:
        raise HTTPException(status_code=409, detail="All payrolls were already archived.")

    # Clear sheet after archiving
    db.query(Payroll).delete()
    db.commit()

    return {
        "message": f"Archived {count} payroll records to history. Payroll sheet has been reset."
    }






# 2. Get all history entries
def get_all_history(db: Session):
    return db.query(PayrollHistory).all()


# 3. Get user-specific history
def get_user_history(user_id: int, db: Session):
    records = db.query(PayrollHistory).filter(PayrollHistory.user_id == user_id).all()
    if not records:
        raise HTTPException(status_code=404, detail="No payroll history found for this user.")
    return records
