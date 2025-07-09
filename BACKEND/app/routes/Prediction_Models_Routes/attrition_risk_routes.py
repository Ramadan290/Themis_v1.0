from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.controllers.Prediction_Models_Controllers.attrition_risk_controller import predict_attrition
from app.models.Prediction_Models_Models.attrition_risk.attrition_risk_history import AttritionRiskHistory

router = APIRouter(prefix="/predict", tags=["AI Predictions"])

@router.post("/attrition/{user_id}")
def predict_attrition_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    _ = Depends(require_role(["admin", "hr"]))
):
    return predict_attrition(user_id, db)



@router.get("/attrition-risk/history/{user_id}")
def get_attrition_risk_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(AttritionRiskHistory)\
                .filter_by(user_id=user_id)\
                .order_by(AttritionRiskHistory.predicted_at.desc())\
                .all()

    if not history:
        raise HTTPException(status_code=404, detail="No attrition prediction history found for this user.")

    return [
        {
            "risk_class": entry.risk_class,
            "risk_level": entry.risk_level,
            "predicted_at": entry.predicted_at
        }
        for entry in history
    ]