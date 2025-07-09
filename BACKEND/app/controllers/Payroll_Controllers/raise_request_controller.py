from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from app.models.Payroll_Models.raise_request_model import RaiseRequest
from app.schemas.Payroll_Schemas.raise_request_schema import RaiseRequestCreate, RaiseRequestReview, RaiseRequestRead
from app.core.utils import generate_uid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

def submit_raise_request(db: Session, request: RaiseRequestCreate, user_role: str):
    payroll = db.query(PayrollFixed).filter(PayrollFixed.user_id == request.user_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="Payroll record for this user not found.")

    max_allowed = payroll.base_salary * Decimal("0.15")
    if request.requested_amount > max_allowed:
        raise HTTPException(status_code=400, detail="Raise exceeds 15% of base salary.")

    raise_request = RaiseRequest(
        payroll_id=payroll.id,
        requested_amount=request.requested_amount,
        reason=request.reason,
        status="pending",
        requested_at=datetime.utcnow(),
        request_uid=generate_uid(prefix="RR"),
        user_id=payroll.user_id  
    )

    db.add(raise_request)
    db.commit()
    db.refresh(raise_request)
    return raise_request


def review_raise_request(db: Session, review: RaiseRequestReview, reviewer_id: int, reviewer_role: str):
    req = db.query(RaiseRequest).filter(RaiseRequest.id == review.request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Raise request not found.")

    # Get the target payroll
    target_payroll = db.query(PayrollFixed).filter(PayrollFixed.id == req.payroll_id).first()
    if not target_payroll:
        raise HTTPException(status_code=404, detail="Linked payroll record not found.")

    # HR cannot approve their own request
    if reviewer_role == "hr" and target_payroll.user_id == reviewer_id:
        raise HTTPException(status_code=403, detail="HR cannot approve their own raise request.")

    if req.status == "approved":
        raise HTTPException(status_code=400, detail="This raise request has already been approved.")
    
    # Apply review data
    req.status = review.status
    req.review_comment = review.review_comment
    req.reviewed_by = reviewer_id
    req.reviewed_at = datetime.utcnow()

    # If approved, update payroll total
    if review.status == "approved":
        target_payroll.total = Decimal(str(target_payroll.total)) + Decimal(str(req.requested_amount))


    db.commit()

    return {"msg": f"Raise request {review.status} successfully."}


def get_raise_requests_by_user_id(db: Session, user_id: int):
    payroll = db.query(PayrollFixed).filter(PayrollFixed.user_id == user_id).first()
    if not payroll:
        raise HTTPException(status_code=404, detail="No payroll found for this user.")

    raise_requests = db.query(RaiseRequest).filter(RaiseRequest.payroll_id == payroll.id).order_by(RaiseRequest.requested_at.desc()).all()
    return raise_requests

def get_all_raise_requests(db: Session):
    return db.query(RaiseRequest).order_by(RaiseRequest.requested_at.desc()).all()