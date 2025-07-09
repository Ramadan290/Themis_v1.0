from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.Payroll_Models.penalty_model import Penalty
from app.models.Payroll_Models.payroll_model import Payroll
from app.schemas.Payroll_Schemas.penalty_schmea import PenaltyCreate, PenaltyRead
from app.database.session import get_db
from app.core.dependencies import get_current_user, require_role
from datetime import datetime
from typing import List

# Add a new penalty
def create_penalty(penalty: PenaltyCreate, db: Session, current_user):
    # Fetch the payroll
    payroll = db.query(Payroll).filter(Payroll.id == penalty.payroll_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll not found.")

    # HR cannot penalize themselves
    if current_user.role == "hr" and payroll.user_id == current_user.id:
        raise HTTPException(status_code=403, detail="HR cannot assign penalty to themselves.")

    # Deduct amount from payroll total
    payroll.total -= float(penalty.amount or 0)

    new_penalty = Penalty(
        payroll_id=penalty.payroll_id,
        amount=penalty.amount,
        reason=penalty.reason
    )
    db.add(new_penalty)
    db.commit()
    db.refresh(new_penalty)
    return new_penalty

# Fetch all penalties for a given user
def get_penalties_by_user_id(user_id: int, db: Session) -> List[PenaltyRead]:
    penalties = (
        db.query(Penalty)
        .join(Payroll)
        .filter(Payroll.user_id == user_id)
        .all()
    )
    if not penalties:
        raise HTTPException(status_code=404, detail="No penalties found for this user.")
    return penalties

def get_all_penalties(db: Session):
    return db.query(Penalty).order_by(Penalty.id.desc()).all()