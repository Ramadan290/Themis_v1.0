from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.User_Models.user_model import User
from app.models.Training_and_Skills_Models.departments_model import Department
from app.models.Training_and_Skills_Models.skills_model import Skill
from app.models.Training_and_Skills_Models.deparments_skill_model import department_skills


# 1. List all users in a department (fixed)
def list_users_in_department(dept_id: int, db: Session):
    users = db.query(User).filter(User.department_id == dept_id).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found in this department")

    return [{"id": user.id, "name": user.username } for user in users]


# 2. Get required skills for a department
def get_required_skills(dept_id: int, db: Session):
    department = db.query(Department).filter(Department.id == dept_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    return [{"id": skill.id, "name": skill.name} for skill in department.skills]


# 3. Display all skills in DB
def list_all_skills(db: Session):
    skills = db.query(Skill).all()
    return [{"id": skill.id, "name": skill.name, "cost_of_training": skill.cost_of_training} for skill in skills]


# 4. Add a new skill
def add_skill(skill_name: str, cost: float, db: Session):
    existing = db.query(Skill).filter(Skill.name == skill_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")

    skill = Skill(name=skill_name, cost_of_training=cost)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return {"id": skill.id, "name": skill.name, "cost_of_training": skill.cost_of_training}


# 5. Remove a skill by ID
def delete_skill(skill_id: int, db: Session):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill)
    db.commit()
    return {"message": f"Skill with ID {skill_id} deleted successfully."}
