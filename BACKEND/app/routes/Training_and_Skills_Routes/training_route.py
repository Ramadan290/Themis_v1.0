from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_role
from app.controllers.Training_and_Skills_Controllers.training_controller import (
    assign_training_to_user,
    get_user_training_status,
    delete_user_training
)

router = APIRouter(prefix="/training", tags=["User Training"])


# 1. Assign a training to a user
@router.post("/assign")
def assign_training(
    body: dict,  # expects { "user_id": int, "training_course_id": int }
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return assign_training_to_user(body["user_id"], body["training_course_id"], db)


# 2. Fetch training status for a user
@router.get("/status/{user_id}")
def get_training_status(
    user_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr", "employee"]))
):
    return get_user_training_status(user_id, db)


# 3. Delete a user training record
@router.delete("/remove/{training_id}")
def remove_training(
    training_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return delete_user_training(training_id, db)
