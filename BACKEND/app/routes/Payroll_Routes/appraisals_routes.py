
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.Payroll_Schemas.appraisals_schema import AppraisalCreate, AppraisalRead
from app.controllers.Payroll_Controllers import appraisals_controller 
from typing import List

router = APIRouter(prefix="/appraisals", tags=["Appraisals"])

@router.post("/add", response_model=AppraisalRead)
def create_appraisal(appraisal: AppraisalCreate, db: Session = Depends(get_db)):
    return appraisals_controller.create_appraisal(appraisal, db)

@router.get("/get/{appraisal_id}", response_model=AppraisalRead)
def read_appraisal(appraisal_id: int, db: Session = Depends(get_db)):
    return appraisals_controller.get_appraisal_by_id(appraisal_id, db)

@router.get("/payroll/{payroll_id}", response_model=List[AppraisalRead])
def read_appraisals_by_payroll(payroll_id: int, db: Session = Depends(get_db)):
    return appraisals_controller.get_appraisals_by_payroll(payroll_id, db)

@router.get("/user/{user_id}", response_model=List[AppraisalRead])
def read_appraisals_by_user(user_id: int, db: Session = Depends(get_db)):
    return appraisals_controller.get_appraisals_by_user_id(user_id, db)



@router.get("/all", response_model=List[AppraisalRead])
def get_all_appraisals(db: Session = Depends(get_db)):
    return appraisals_controller.get_all_appraisals(db)
