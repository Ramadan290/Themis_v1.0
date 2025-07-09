"""
Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - Posting a comment on a news Post (All)
 - Deleting a comment from a News Post (Admin & oneself)

"""

\
from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from app.schemas.Payroll_Schemas.payroll_fixed_schema import (
    PayrollFixedCreate,
    PayrollFixedOut,
    PayrollFixedUpdate
)

from app.controllers.Payroll_Controllers import payroll_fixed_controller
from app.core.dependencies import get_db , require_role



router = APIRouter(
    prefix="/payroll-fixed",
    tags=["Payroll Fixed"]
)


@router.post("/generate")
def generate_fixed_salaries(
    default_salary: float = Body(..., embed=True),
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    return payroll_fixed_controller.generate_fixed_salaries(default_salary, db)


@router.put("/update/{user_id}", response_model=PayrollFixedOut)
def update_fixed_salary(
    user_id: int = Path(...),
    data: PayrollFixedUpdate = Body(...),
    db: Session = Depends(get_db),
    user = Depends(require_role("admin,hr"))
):
    return payroll_fixed_controller.update_fixed_entry(user_id, data, db)


@router.get("/get/all", response_model=list[PayrollFixedOut])
def get_all_fixed_salaries(
    db: Session = Depends(get_db),
    user = Depends(require_role("admin,hr"))
):
    return payroll_fixed_controller.get_all_fixed(db)


@router.get("/get/{user_id}", response_model=PayrollFixedOut)
def get_fixed_salary_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin,hr,employee"))  # ✅ allow employee too
):
    return payroll_fixed_controller.get_fixed_by_user(user_id, db, user)
