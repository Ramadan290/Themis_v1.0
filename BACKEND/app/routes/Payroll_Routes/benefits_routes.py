
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.Payroll_Controllers import benefits_controller
from app.schemas.Payroll_Schemas.benefits_schema import BenefitCreate
from app.core.dependencies import get_db, require_role

router = APIRouter(prefix="/benefit", tags=["Benefits"])

@router.post("/assign", dependencies=[Depends(require_role(["admin", "hr"]))])
def assign_benefit(benefit: BenefitCreate, db: Session = Depends(get_db)):
    return benefits_controller.assign_benefit_to_user(benefit, db)

@router.get("/user/{user_id}", dependencies=[Depends(require_role(["admin", "hr" , "employee"]))])
def get_user_benefits(user_id: int, db: Session = Depends(get_db)):
    return benefits_controller.get_user_benefits(user_id, db)
