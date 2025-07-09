import numpy as np
from sqlalchemy.orm import Session
import tensorflow as tf
from app.models.Prediction_Models_Models.performance_prediction.performance_prediction_history import PerformancePredictionHistory
from app.models.Prediction_Models_Models.performance_prediction.current_performance_prediction import CurrentPerformancePrediction
from app.models.Training_and_Skills_Models.user_training_model import UserTraining
from app.models.User_Models.performance_metrics_model import PerformanceMetric
from app.models.User_Models.personal_data_model import PersonalData
from app.models.Payroll_Models.penalty_model import Penalty
from app.models.Payroll_Models.raise_request_model import RaiseRequest
from app.models.Payroll_Models.appraisals_model import Appraisal
from app.models.Attendance_Models.sick_note_model import SickNote
from app.models.Payroll_Models.benefits_model import Benefit
from app.models.Prediction_Models_Models.sentiment_analysis.current_sentiment_score import CurrentSentimentScore
from app.core.utils import suppress_tf_lite_logs , suppress_stderr



#Load TFLite Model
with suppress_stderr():
    interpreter = tf.lite.Interpreter(
        model_path="app/prediction_models/performance_prediction.tflite",
        experimental_delegates=[]  
    )
    interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def predict_performance(user_id: int, db: Session):
    with suppress_stderr():
        interpreter = tf.lite.Interpreter(
            model_path="app/prediction_models/performance_prediction.tflite",
            experimental_delegates=[]
        )
        interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # === Fetch all inputs or use defaults ===
    perf_metric = db.query(PerformanceMetric).filter_by(user_id=user_id).first()
    penalties = db.query(Penalty).filter_by(user_id=user_id).count()
    raise_requests = db.query(RaiseRequest).filter_by(user_id=user_id).count()
    appraisals = db.query(Appraisal).filter_by(user_id=user_id).all()
    sick_notes = db.query(SickNote).filter_by(user_id=user_id).count()
    benefits = db.query(Benefit).filter_by(user_id=user_id).count()
    sentiment = db.query(CurrentSentimentScore).filter_by(user_id=user_id).first()
    personal_data = db.query(PersonalData).filter_by(user_id=user_id).first()

    # Required: fallback simulation if missing
    completion_rate = perf_metric.completion_rate if perf_metric else 0.75
    appraisal_amount = sum([a.amount for a in appraisals]) if appraisals else 0.0
    months_at_company = personal_data.months_at_company if personal_data else 6
    sentiment_score = sentiment.sentiment_score if sentiment else 2

    # Optional debug print if simulating
    if not perf_metric:
        print(f"[ℹ️] Simulated completion_rate for user {user_id}")
    if not appraisals:
        print(f"[ℹ️] Simulated appraisal_amount for user {user_id}")
    if not personal_data:
        print(f"[ℹ️] Simulated months_at_company for user {user_id}")
    if not sentiment:
        print(f"[ℹ️] Simulated sentiment_score for user {user_id}")

    # === Construct input vector ===
    input_vector = np.array([[ 
        completion_rate,     # From PerformanceMetric or default
        penalties,           # count
        raise_requests,      # count
        appraisal_amount,    # sum
        sick_notes,          # count
        benefits,            # count
        months_at_company,   # From PersonalData or default
        sentiment_score      # From Sentiment table or default
    ]], dtype=np.float32)

    print("📥 Input Vector:", input_vector)

    # === Run Inference ===
    interpreter.set_tensor(input_details[0]['index'], input_vector)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index']).copy()
    print("🔮 Raw Model Output (Softmax):", output[0])

    predicted_class = int(np.argmax(output[0]))

    # === Save or Update current prediction ===
    existing = db.query(CurrentPerformancePrediction).filter_by(user_id=user_id).first()
    if existing:
        existing.performance_score = predicted_class
    else:
        db.add(CurrentPerformancePrediction(user_id=user_id, performance_score=predicted_class))

    # === Log History ===
    db.add(PerformancePredictionHistory(user_id=user_id, performance_score=predicted_class))
    db.commit()

    return {"user_id": user_id, "performance_score": predicted_class}
