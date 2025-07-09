from pydantic import BaseModel, Field
from typing import Optional, List


class TrainingAndSkillsBase(BaseModel):
    completion_rate: float = Field(..., ge=0.0, le=1.0)
    has_training: bool
    cost_of_training: float = Field(..., ge=0.0)

class TrainingAndSkillsCreate(TrainingAndSkillsBase):
    user_id: int

class TrainingAndSkillsInput(BaseModel):
    completion_rate: float = Field(..., ge=0.0, le=1.0)
    has_training: bool
    cost_of_training: float = Field(..., ge=0.0)    

class TrainingAndSkillsRead(TrainingAndSkillsBase):
    user_id: int

    class Config:
        from_attributes = True