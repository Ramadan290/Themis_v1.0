from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.Payroll_Schemas.raise_request_schema import RaiseRequestCreate, RaiseRequestReview, RaiseRequestRead
from app.controllers.Payroll_Controllers import raise_request_controller
from app.core.dependencies import get_db, get_current_user, require_role
from typing import List

router = APIRouter(prefix="/raise", tags=["Raise Requests"])


@router.post("/submit", response_model=RaiseRequestRead)
def submit_raise(
    req: RaiseRequestCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return raise_request_controller.submit_raise_request(db, req, current_user.role)


@router.post("/review")
def review_raise(
    review_data: RaiseRequestReview,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin", "hr"]))
):
    return raise_request_controller.review_raise_request(db, review_data, current_user.id, current_user.role)


@router.get("/user/{user_id}", response_model=List[RaiseRequestRead])
def fetch_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return raise_request_controller.get_raise_requests_by_user_id(db, user_id)

@router.get("/all", response_model=List[RaiseRequestRead], summary="Get all raise requests (unfiltered)")
def get_all_raise_requests(
    db: Session = Depends(get_db)
):
    return raise_request_controller.get_all_raise_requests(db)
