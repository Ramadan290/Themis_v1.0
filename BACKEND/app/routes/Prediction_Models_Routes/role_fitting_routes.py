from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.controllers.Prediction_Models_Controllers.role_fitting_controller import predict_fit_score
from app.models.User_Models.user_model import User
from app.models.Training_and_Skills_Models.departments_model import Department

router = APIRouter(prefix="/predict", tags=["AI Predictions"])

@router.post("/role-fitting/{user_id}")
def role_fitting_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    _ = Depends(require_role(["admin", "hr"]))
):
    return predict_fit_score(user_id, db)




@router.put("/role-fitting/transfer/{user_id}")
def transfer_user_department(user_id: int, new_department: str, db: Session = Depends(get_db)):
    # Only HR or Admin should access this — add role check if needed

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dept = db.query(Department).filter(Department.name == new_department).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Target department not found")

    user.department_id = dept.id
    db.commit()

    return {
        "message": f"User {user.username} has been successfully transferred to {new_department}.",
        "user_id": user.id,
        "new_department": new_department
    }


