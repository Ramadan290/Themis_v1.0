"""
Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - Posting a comment on a news Post (All)
 - Deleting a comment from a News Post (Admin & oneself)

"""

from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.orm import Session
from app.schemas.Payroll_Schemas.payroll_schema import PayrollCreate, PayrollOut , PayrollUpdate
from app.controllers.Payroll_Controllers import payroll_controller
from app.core.dependencies import get_db, get_current_user , require_role

router = APIRouter(
    prefix="/payroll",
    tags=["Payroll"]
)


# Create payroll sheet for all users (Admin + HR)
@router.post("/sheet")
def create_payroll_sheet(
    db: Session = Depends(get_db),
    user = Depends(require_role("admin,hr"))
):
    return payroll_controller.create_payroll_sheet(db)


# Update payroll by payroll ID (Admin + HR)
@router.put("/sheet/update/{payroll_id}", response_model=PayrollOut)
def update_payroll(
    payroll_id: int = Path(...),
    payroll_data: PayrollUpdate = Body(...),
    db: Session = Depends(get_db),
    user = Depends(require_role("admin,hr"))
):
    return payroll_controller.update_payroll(payroll_id, payroll_data, db)


# Get payroll by user ID (All roles)
@router.get("/sheet/user/{user_id}", response_model=PayrollOut)
def get_payroll_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return payroll_controller.get_payroll_by_user(user_id, db)


# Get all payroll records (Admin only)
@router.get("/sheet/all", response_model=list[PayrollOut])
def get_all_payrolls(
    db: Session = Depends(get_db),
    user = Depends(require_role("admin,hr"))
):
    return payroll_controller.get_all_payrolls(db)
