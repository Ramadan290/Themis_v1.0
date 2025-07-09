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
from app.models.User_Models.user_model import User
from app.schemas.Payroll_Schemas.payroll_schema import PayrollCreate
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed


from datetime import datetime
import random
def create_payroll_sheet(db: Session, period: str):
    users = db.query(User).all()
    added_count = 0

    # ✅ Use passed-in period
    year, month = map(int, period.split('-'))

    for user in users:
        # Skip if payroll for this period already exists
        existing = db.query(Payroll).filter(
            Payroll.user_id == user.id,
            Payroll.created_at.between(
                datetime(year, month, 1),
                datetime(year, month, 28, 23, 59, 59)
            )
        ).first()
        if existing:
            continue

        # ✅ Use the simulated period to generate created_at
        simulated_day = random.randint(1, 28)
        created_at = datetime(year, month, simulated_day)

        fixed = db.query(PayrollFixed).filter(PayrollFixed.user_id == user.id).first()
        if not fixed:
            continue

        new_payroll = Payroll(
            user_id=user.id,
            salary=fixed.base_salary,
            status="draft",
            created_at=created_at,
            last_updated=created_at
        )
        db.add(new_payroll)
        added_count += 1

    db.commit()

    if added_count == 0:
        raise HTTPException(
            status_code=400,
            detail=f"No payroll entries created for simulated period {period}. All users already processed or missing fixed salaries."
        )

    return {"message": f"Payroll sheet for simulated period {period} created for {added_count} users."}


# Update payroll record
def update_payroll(payroll_id: int, data: PayrollCreate, db: Session):
    payroll = db.query(Payroll).filter(Payroll.id == payroll_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll record not found.")

    if data.salary is not None:
        payroll.salary = data.salary
    if data.status:
        payroll.status = data.status

    payroll.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(payroll)
    return payroll


# Get payroll by user ID 
def get_payroll_by_user(user_id: int, db: Session):
    payroll = db.query(Payroll).filter(Payroll.user_id == user_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll not found.")
    return payroll


# Get all payroll records
def get_all_payrolls(db: Session):
    return db.query(Payroll).all()
