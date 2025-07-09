from pydantic import BaseModel, Field
from typing import Optional, List

class UserSkillBase(BaseModel):
    skill_name: str
    skill_level: int = Field(..., ge=0, le=10)

class UserSkillCreate(UserSkillBase):
    user_id: int

class UserSkillRead(UserSkillBase):
    id: int
    user_id: int

class AssignSkillInput(BaseModel):
    skill_name: str = Field(..., example="Python")
    level: int = Field(default=5, ge=0, le=10)

    class Config:
        from_attributes = True