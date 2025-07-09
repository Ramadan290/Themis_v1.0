from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.Training_and_Skills_Models.user_skills_model import UserSkill
from app.models.Training_and_Skills_Models.skills_model import Skill



# 1. Fetch User Skills
def fetch_user_skills(user_id: int, db: Session):
    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    result = []

    for entry in user_skills:
        skill = db.query(Skill).filter(Skill.id == entry.skill_id).first()
        if skill:
            result.append({
                "id": skill.id,
                "user_id": user_id,
                "skill_name": skill.name,
                "skill_level": entry.skill_level
            })
    return result


# 2. Assign Skill to User
def assign_skill_to_user(user_id: int, skill_name: str, level: int, db: Session):
    skill = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill:
        skill = Skill(name=skill_name)
        db.add(skill)
        db.commit()
        db.refresh(skill)

    user_skill = UserSkill(user_id=user_id, skill_id=skill.id, skill_level=level)
    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)

    return {
        "id": skill.id,
        "user_id": user_id,
        "skill_name": skill.name,
        "skill_level": level
    }
