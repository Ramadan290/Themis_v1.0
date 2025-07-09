from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.Training_and_Skills_Models.user_training_model import UserTraining


# 1. Add a training course to a user
def assign_training_to_user(user_id: int, training_course_id: int, db: Session):
    existing = db.query(UserTraining).filter(
        UserTraining.user_id == user_id,
        UserTraining.training_course_id == training_course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User is already enrolled in this course")

    training = UserTraining(
        user_id=user_id,
        training_course_id=training_course_id,
        completed=False,
        progress=0.0,
        score=None,
        cost_of_training=None
    )
    db.add(training)
    db.commit()
    db.refresh(training)

    return {
        "message": f"Training course {training_course_id} assigned to user {user_id}",
        "training_id": training.id
    }


# 2. Fetch user's training status
def get_user_training_status(user_id: int, db: Session):
    trainings = db.query(UserTraining).filter(UserTraining.user_id == user_id).all()
    if not trainings:
        return []

    return [{
        "training_id": t.id,
        "training_course_id": t.training_course_id,
        "completed": t.completed,
        "progress": t.progress,
        "score": t.score,
        "cost_of_training": t.cost_of_training
    } for t in trainings]


# 3. Delete user's training record
def delete_user_training(training_id: int, db: Session):
    training = db.query(UserTraining).filter(UserTraining.id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail="Training record not found")

    db.delete(training)
    db.commit()
    return {"message": f"Training record {training_id} deleted successfully"}
