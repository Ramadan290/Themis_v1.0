from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user, require_role
from app.controllers.Prediction_Models_Controllers.sentiment_score_controller import predict_sentiment_score
from app.models.Prediction_Models_Models.sentiment_analysis.sentiment_score_historical import SentimentScoreHistory

router = APIRouter(prefix="/predict", tags=["AI Predictions"])

@router.post("/sentiment_score/{user_id}")
def predict_sentiment_score_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    _ = Depends(require_role(["admin", "hr"]))
):
    result = predict_sentiment_score(db, user_id)

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@router.get("/sentiment-score/history/{user_id}")
def get_sentiment_score_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(SentimentScoreHistory)\
                .filter_by(user_id=user_id)\
                .order_by(SentimentScoreHistory.predicted_at.desc())\
                .all()

    if not history:
        raise HTTPException(status_code=404, detail="No sentiment prediction history found for this user.")

    return [
        {
            "sentiment_score": entry.sentiment_score,
            "predicted_at": entry.predicted_at
        }
        for entry in history
    ]