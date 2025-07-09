from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.controllers.Prediction_Models_Controllers.benefit_to_cost_ratio_controller import predict_bcr
from app.models.Prediction_Models_Models.benefit_to_cost_ratio.benefit_to_cost_ratio_history import BenefitCostRatioHistory


router = APIRouter(prefix="/predict", tags=["AI Predictions"])

@router.post("/bcr/{user_id}")
def predict_bcr_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    _ = Depends(require_role(["admin", "hr"]))
):
    return predict_bcr(user_id, db)


@router.get("/bcr/history/{user_id}")
def get_bcr_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(BenefitCostRatioHistory)\
                .filter_by(user_id=user_id)\
                .order_by(BenefitCostRatioHistory.predicted_at.desc())\
                .all()

    if not history:
        raise HTTPException(status_code=404, detail="No BCR prediction history found for this user.")

    return [
        {
            "bcr_score": entry.bcr_score,
            "predicted_at": entry.predicted_at
        }
        for entry in history
    ]