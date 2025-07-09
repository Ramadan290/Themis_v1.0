from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, require_role

from app.controllers.Training_and_Skills_Controllers.department_skill_controller import (
    list_users_in_department,
    get_required_skills,
    list_all_skills,
    add_skill,
    delete_skill
)

router = APIRouter(prefix="/departments", tags=["Departments & Skills"])


@router.get("/{dept_id}/users")
def get_department_users(
    dept_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return list_users_in_department(dept_id, db)


@router.get("/{dept_id}/required-skills")
def get_department_required_skills(
    dept_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return get_required_skills(dept_id, db)


@router.get("/skills/all")
def get_all_skills(
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr", "employee"]))
):
    return list_all_skills(db)


@router.post("/skills/add")
def post_new_skill(
    body: dict,  # expects: {"skill_name": ..., "cost": ...}
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return add_skill(body["skill_name"], body["cost"], db)


@router.delete("/skills/remove/{skill_id}")
def remove_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return delete_skill(skill_id, db)
