from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.Training_and_Skills_Models.skills_model import Skill
from app.models.Training_and_Skills_Models.training_courses_model import TrainingCourse
from app.schemas.Training_and_Skills_Schemas.training_courses_schema import TrainingCourseCreate, TrainingCourseRead


# 1. Fetch All Courses
def get_all_training_courses(db: Session) -> list[TrainingCourseRead]:
    courses = db.query(TrainingCourse).all()
    result = []

    for course in courses:
        skill = db.query(Skill).filter(Skill.id == course.skill_id).first()
        result.append(TrainingCourseRead(
            id=course.id,
            course_name=course.course_name,
            skill_targeted=skill.name if skill else "Unknown",
            difficulty_level=course.difficulty_level,
            cost=course.cost,
            duration_days=course.duration_days
        ))

    return result


# 2. Add New Course
def create_training_course(db: Session, data: TrainingCourseCreate) -> TrainingCourseRead:
    skill = db.query(Skill).filter(Skill.name == data.skill_targeted).first()
    if not skill:
        skill = Skill(name=data.skill_targeted)
        db.add(skill)
        db.commit()
        db.refresh(skill)

    # Create the course
    course = TrainingCourse(
        course_name=data.course_name,
        skill_id=skill.id,
        difficulty_level=data.difficulty_level,
        cost=data.cost,
        duration_days=data.duration_days
    )
    db.add(course)

    # ✅ Sync skill cost
    skill.cost_of_training = data.cost  # ← This line ensures consistency

    db.commit()
    db.refresh(course)

    return TrainingCourseRead(
        id=course.id,
        course_name=course.course_name,
        skill_targeted=skill.name,
        difficulty_level=course.difficulty_level,
        cost=course.cost,
        duration_days=course.duration_days
    )



# 3. Delete Course
def delete_training_course(db: Session, course_id: int) -> dict:
    course = db.query(TrainingCourse).filter(TrainingCourse.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return {"message": f"Course with ID {course_id} deleted successfully."}
