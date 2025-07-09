from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.Payroll_Schemas.penalty_schmea import PenaltyCreate, PenaltyRead
from app.controllers.Payroll_Controllers import penalty_controller 
from app.core.dependencies import require_role
from typing import List

router = APIRouter(prefix="/penalties", tags=["Penalties"])


@router.post("/add", response_model=PenaltyRead)
def create_penalty(
    penalty: PenaltyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["hr", "admin"]))
):
    return penalty_controller.create_penalty(penalty, db, current_user)

@router.get("/user/{user_id}", response_model=List[PenaltyRead])
def read_penalties_by_user(user_id: int, db: Session = Depends(get_db)):
    return penalty_controller.get_penalties_by_user_id(user_id, db)


@router.get("/all", response_model=List[PenaltyRead])
def get_all_penalties(db: Session = Depends(get_db)):
    return penalty_controller.get_all_penalties(db)

