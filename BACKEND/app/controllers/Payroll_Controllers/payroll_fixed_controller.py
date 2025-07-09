""""
Controllers are responsible for the application logic that is sent to routes and proccessed at request .

A future enhancement would be to implement services and seperate business logic but this is not necessary 
right now we dont have that many features so eveyrthing can be handled in controllers.

This File includes : 




"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from app.schemas.Payroll_Schemas.payroll_fixed_schema import PayrollFixedCreate, PayrollFixedUpdate
from app.models.User_Models.user_model import User  
from app.models.Payroll_Models.benefit_catalog_model import BenefitCatalog
from app.controllers.Payroll_Controllers import benefits_controller
from app.models.Payroll_Models.benefits_model import Benefit


def generate_fixed_salaries(default_salary: float, db: Session):
    users = db.query(User).all()
    added_count = 0

    for user in users:
        # Skip if already exists
        if db.query(PayrollFixed).filter(PayrollFixed.user_id == user.id).first():
            continue

        # ✅ Add default benefits if user has none
        if not db.query(Benefit).filter(Benefit.user_id == user.id).first():
            benefits_controller.add_default_benefits(user.id, db)

        # ✅ Fetch all benefits assigned to user (joined with catalog)
        benefits = (
            db.query(Benefit)
            .filter(Benefit.user_id == user.id)
            .join(BenefitCatalog, Benefit.benefit_catalog_id == BenefitCatalog.id)
            .all()
        )

        # ✅ Sum amounts based on catalog values
        benefit_total = sum(
            db.query(BenefitCatalog.default_amount)
            .filter(BenefitCatalog.id == b.benefit_catalog_id)
            .scalar()
            for b in benefits
        )

        total_salary = default_salary + benefit_total

        new_payroll = PayrollFixed(
            user_id=user.id,
            base_salary=default_salary,
            total=total_salary
        )

        db.add(new_payroll)
        db.commit()
        added_count += 1

    if added_count == 0:
        return {"message": "All users already have fixed salaries. Nothing was added."}

    return {"message": f"Base salaries generated for {added_count} users including default benefits."}



def update_fixed_entry(user_id: int, data: PayrollFixedUpdate, db: Session):
    entry = db.query(PayrollFixed).filter(PayrollFixed.user_id == user_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Fixed payroll entry not found.")

    entry.base_salary = data.base_salary
    db.commit()
    db.refresh(entry)
    return entry


def get_all_fixed(db: Session):
    return db.query(PayrollFixed).all()


def get_fixed_by_user(user_id: int, db: Session, current_user):
    # Restrict access if employee tries to view someone else's data
    if current_user.role == "employee" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this payroll data.")

    payroll = db.query(PayrollFixed).filter_by(user_id=user_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll record not found.")
    
    return payroll