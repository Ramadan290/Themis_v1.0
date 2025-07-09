import numpy as np
import tensorflow as tf
from sqlalchemy.orm import Session

from app.models.Prediction_Models_Models.attrition_risk.attrition_risk_history import AttritionRiskHistory
from app.models.Prediction_Models_Models.attrition_risk.current_attrition_risk import CurrentAttritionRisk
from app.models.User_Models.personal_data_model import PersonalData
from app.models.Prediction_Models_Models.sentiment_analysis.current_sentiment_score import CurrentSentimentScore
from app.models.Training_and_Skills_Models.user_training_model import UserTraining
from app.models.Payroll_Models.appraisals_model import Appraisal
from app.models.Payroll_Models.raise_request_model import RaiseRequest
from app.models.User_Models.performance_metrics_model import PerformanceMetric
from app.models.Payroll_Models.penalty_model import Penalty
from app.models.Payroll_Models.benefits_model import Benefit
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from app.models.Prediction_Models_Models.performance_prediction.current_performance_prediction import CurrentPerformancePrediction


def predict_attrition(user_id: int, db: Session):
    interpreter = tf.lite.Interpreter(model_path="app/prediction_models/attrition_risk.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    # Fetch data
    personal = db.query(PersonalData).filter_by(user_id=user_id).first()
    sentiment = db.query(CurrentSentimentScore).filter_by(user_id=user_id).first()
    training = db.query(UserTraining).filter_by(user_id=user_id).first()
    perf_metric =  db.query(PerformanceMetric).filter_by(user_id=user_id).first()
    payroll = db.query(PayrollFixed).filter_by(user_id=user_id).first()
    performance = db.query(CurrentPerformancePrediction).filter_by(user_id=user_id).first()

    if not (personal and sentiment and training and payroll and performance):
        return {"error": f"Missing required inputs for user {user_id}"}

    appraisals = db.query(Appraisal).filter_by(user_id=user_id).count()
    penalties = db.query(Penalty).filter_by(user_id=user_id).count()
    raises = db.query(RaiseRequest).filter_by(user_id=user_id).count()
    benefits = db.query(Benefit).filter_by(user_id=user_id).count()

    # Encode categorical
    gender_encoded = 1 if personal.gender.lower() == 'male' else 0
    marital_encoded = 1 if personal.marital_status.lower() == 'single' else 0

    # Prepare input
    input_vector = np.array([[ 
        personal.age,
        gender_encoded,
        marital_encoded,
        personal.months_at_company,
        appraisals,
        float(payroll.base_salary),
        penalties,
        raises,
        benefits,
        performance.performance_score,
        sentiment.sentiment_score,
        perf_metric.completion_rate,
        perf_metric.completion_rate  # placeholder for attendance_rate
    ]], dtype=np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_vector)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index']).copy()

    # Prediction
    predicted_class = int(np.argmax(output[0]))
    predicted_class = max(0, min(3, predicted_class))

    # Risk label
    level_map = ["Low", "Medium", "High", "Critical"]
    risk_label = level_map[predicted_class]

    # Update current
    existing = db.query(CurrentAttritionRisk).filter_by(user_id=user_id).first()
    if existing:
        existing.risk_class = predicted_class
        existing.risk_level = risk_label
    else:
        db.add(CurrentAttritionRisk(
            user_id=user_id,
            risk_class=predicted_class,
            risk_level=risk_label
        ))

    # Add to history
    db.add(AttritionRiskHistory(
        user_id=user_id,
        risk_class=predicted_class,
        risk_level=risk_label
    ))

    db.commit()

    return {
        "user_id": user_id,
        "risk_class": predicted_class,
        "risk_level": risk_label
    }
