from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core.dependencies import require_role
from app.schemas.Training_and_Skills_Schemas.training_courses_schema import (
    TrainingCourseCreate,
    TrainingCourseRead
)
from app.controllers.Training_and_Skills_Controllers.training_courses_controller import (
    get_all_training_courses,
    create_training_course,
    delete_training_course
)

router = APIRouter(prefix="/skills", tags=["Skills & Training"])


# GET all courses
@router.get("/courses", response_model=List[TrainingCourseRead])
def get_courses(
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return get_all_training_courses(db)


# POST add new course
@router.post("/courses", response_model=TrainingCourseRead)
def add_course(
    course: TrainingCourseCreate,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return create_training_course(db, course)


# DELETE a course by ID
@router.delete("/courses/{course_id}")
def remove_course(
    course_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return delete_training_course(db, course_id)
