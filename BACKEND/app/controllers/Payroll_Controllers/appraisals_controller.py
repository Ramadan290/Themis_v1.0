from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.Payroll_Models.appraisals_model import Appraisal
from app.schemas.Payroll_Schemas.appraisals_schema import AppraisalCreate, AppraisalRead
from app.database.session import get_db
from app.models.Payroll_Models.payroll_model import Payroll
from app.core.dependencies import get_current_user, require_role
from datetime import datetime
from typing import List



# Add Appraisal
def create_appraisal(appraisal: AppraisalCreate, db: Session, current_user=Depends(require_role(["hr", "admin"]))):
    existing = db.query(Appraisal).filter(Appraisal.payroll_id == appraisal.payroll_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Appraisal already exists for this payroll.")

    # Fetch payroll and update total
    payroll = db.query(Payroll).filter(Payroll.id == appraisal.payroll_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll not found.")

    payroll.total += appraisal.amount or 0

    new_appraisal = Appraisal(
        payroll_id=appraisal.payroll_id,
        amount=appraisal.amount,
        appraisal_date=appraisal.appraisal_date or datetime.utcnow()
    )
    db.add(new_appraisal)
    db.commit()
    db.refresh(new_appraisal)
    return new_appraisal


# Get single appraisal
def get_appraisal_by_id(appraisal_id: int, db: Session, current_user=Depends(get_current_user)):
    appraisal = db.query(Appraisal).filter(Appraisal.id == appraisal_id).first()
    if not appraisal:
        raise HTTPException(status_code=404, detail="Appraisal not found.")
    return appraisal

# Get all appraisals for a specific payroll
def get_appraisals_by_payroll(payroll_id: int, db: Session, current_user=Depends(get_current_user)) -> List[AppraisalRead]:
    return db.query(Appraisal).filter(Appraisal.payroll_id == payroll_id).all()


# Get all appraisals by user id 
def get_appraisals_by_user_id(user_id: int, db: Session):
    appraisals = (
        db.query(Appraisal)
        .join(Payroll)
        .filter(Payroll.user_id == user_id)
        .all()
    )

    if not appraisals:
        raise HTTPException(status_code=404, detail="No appraisals found for this user.")

    return appraisals


def get_all_appraisals(db: Session):
    return db.query(Appraisal).order_by(Appraisal.appraisal_date.desc()).all()
