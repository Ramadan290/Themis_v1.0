from pydantic import BaseModel, Field
from typing import Optional, List


class TrainingCourseBase(BaseModel):
    course_name: str
    skill_targeted: str
    difficulty_level: int = Field(..., ge=1, le=5)
    cost: float = Field(..., ge=0.0)
    duration_days: int = Field(..., gt=0)

class TrainingCourseCreate(TrainingCourseBase):
    pass

class TrainingCourseRead(TrainingCourseBase):
    id: int




    class Config:
        from_attributes = True