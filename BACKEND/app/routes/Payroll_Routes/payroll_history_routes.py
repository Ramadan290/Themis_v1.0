"""
Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - Posting a comment on a news Post (All)
 - Deleting a comment from a News Post (Admin & oneself)

"""


from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.orm import Session
from app.core.dependencies import get_db , require_role
from app.controllers.Payroll_Controllers import payroll_history_controller
from app.schemas.Payroll_Schemas.payroll_history_schema import PayrollHistoryOut

router = APIRouter(
    prefix="/payroll-history",
    tags=["Payroll History"]
)


# 1. Archive approved payroll to history
@router.post("/process")
def process_payroll_history(
    period: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    user = Depends(require_role("admin , hr"))
):
    return payroll_history_controller.process_payroll_to_history(period, db)


# 2. Get all payroll history (admina and hr)
@router.get("/all", response_model=list[PayrollHistoryOut])
def get_all_payroll_history(
    db: Session = Depends(get_db),
    user = Depends(require_role("admin , hr"))
):
    return payroll_history_controller.get_all_history(db)


# 3. Get history by user (admin/hr)
@router.get("/user/{user_id}", response_model=list[PayrollHistoryOut])
def get_user_payroll_history(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    user = Depends(require_role("admin , hr , employee"))
):
    return payroll_history_controller.get_user_history(user_id, db)
