from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.controllers.Prediction_Models_Controllers.performance_prediction_controller import predict_performance
from app.models.Prediction_Models_Models.performance_prediction.performance_prediction_history import PerformancePredictionHistory


router = APIRouter(prefix="/predict", tags=["AI Predictions"])

@router.post("/performance/{user_id}")
def predict_performance_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    _ = Depends(require_role(["admin", "hr"]))
):
    return predict_performance(user_id, db)



@router.get("/performance/history/{user_id}")
def get_performance_score_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(PerformancePredictionHistory)\
                .filter_by(user_id=user_id)\
                .order_by(PerformancePredictionHistory.predicted_at.desc())\
                .all()
    
    if not history:
        raise HTTPException(status_code=404, detail="No performance prediction history found for this user.")

    return [
        {
            "performance_score": entry.performance_score,
            "predicted_at": entry.predicted_at
        }
        for entry in history
    ]