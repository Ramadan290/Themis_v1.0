from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import require_role
from app.controllers.Training_and_Skills_Controllers.user_skills_controller import (
    fetch_user_skills,
    assign_skill_to_user
)

router = APIRouter(prefix="/skills", tags=["User Skills & Training"])


# 1. Fetch User Skills
@router.get("/user-skills/{user_id}")
def get_user_skills(
    user_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr", "employee"]))
):
    return fetch_user_skills(user_id, db)


# 2. Assign Skill to User
@router.post("/assign-skill/{user_id}")
def assign_skill(
    user_id: int,
    body: dict,  # expects: {"skill_name": ..., "level": ...}
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return assign_skill_to_user(user_id, body["skill_name"], body["level"], db)