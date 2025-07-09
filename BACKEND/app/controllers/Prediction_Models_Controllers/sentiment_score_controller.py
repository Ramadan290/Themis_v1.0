import numpy as np
import tensorflow as tf
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.User_Models.sentiment_inputs_model import SentimentInput
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from app.models.Payroll_Models.appraisals_model import Appraisal
from app.models.Payroll_Models.raise_request_model import RaiseRequest
from app.models.Payroll_Models.benefits_model import Benefit
from app.models.Payroll_Models.penalty_model import Penalty
from app.models.User_Models.personal_data_model import PersonalData
from app.models.Training_and_Skills_Models.user_skills_model import UserSkill
from app.models.Training_and_Skills_Models.user_training_model import UserTraining
from app.models.Prediction_Models_Models.performance_prediction.current_performance_prediction import CurrentPerformancePrediction
from app.models.Prediction_Models_Models.attrition_risk.current_attrition_risk import CurrentAttritionRisk
from app.models.News_Models.comment_model import Comment
from app.models.User_Models.performance_metrics_model import PerformanceMetric

from app.models.Attendance_Models.attendance_history_model import AttendanceHistory
from app.models.Prediction_Models_Models.sentiment_analysis.current_sentiment_score import CurrentSentimentScore
from app.models.Prediction_Models_Models.sentiment_analysis.sentiment_score_historical import SentimentScoreHistory
from datetime import datetime
from app.models.Attendance_Models.sick_note_model import SickNote
from tensorflow.keras.models import load_model # type: ignore


from app.core.tf import pad_text_sequences
from app.core.tokenizer import tokenizer


def load_interpreter(path):
    interpreter = tf.lite.Interpreter(model_path=path)
    interpreter.allocate_tensors()
    return interpreter

def get_input_output_details(interpreter):
    return interpreter.get_input_details(), interpreter.get_output_details()

def predict_sentiment_score(db: Session, user_id: int):
    # === Lazy Load TFLite Models ===
    interpreter_struct = load_interpreter("app/prediction_models/structured_model_latent.tflite")
    interpreter_text = load_interpreter("app/prediction_models/textual_model_latent.tflite")
    interpreter_fusion = load_interpreter("app/prediction_models/classifier_model.tflite")

    

    # === Fetch User Inputs from DB ===
    sentiment_row = db.query(SentimentInput).filter_by(user_id=user_id).order_by(SentimentInput.recorded_at.desc()).first()
    payroll = db.query(PayrollFixed).filter_by(user_id=user_id).first()
    training = db.query(UserTraining).filter_by(user_id=user_id).first()

    # NEW: Dynamically calculate has_training
    has_training = db.query(UserTraining).filter_by(user_id=user_id, completed=True).first() is not None
    
    perf_metric =  db.query(PerformanceMetric).filter_by(user_id=user_id).first()
    performance = db.query(CurrentPerformancePrediction).filter_by(user_id=user_id).first()
    attrition = db.query(CurrentAttritionRisk).filter_by(user_id=user_id).first()

    if not (sentiment_row and payroll and training and performance and attrition):
        return {"error": "Missing required inputs for prediction."}

    appraisals = db.query(Appraisal).filter_by(user_id=user_id).count()
    raises = db.query(RaiseRequest).filter_by(user_id=user_id).count()
    benefits = db.query(Benefit).filter_by(user_id=user_id).count()
    penalties = db.query(Penalty).filter_by(user_id=user_id).count()
    comments = db.query(Comment).filter_by(user_id=user_id).count()

    stress_level = attrition.risk_class
    interaction_fields = [
        str(sentiment_row.recorded_speech_positive or ""),
        str(sentiment_row.recorded_speech_negative or ""),
        str(sentiment_row.interaction_example or ""),
        str(sentiment_row.meeting_idea or ""),
        str(sentiment_row.movement_type or ""),
        str(sentiment_row.sitting_posture or ""),
    ]
    total_num_of_interactions = comments + sum(1 for field in interaction_fields if field and field.strip())

    total_days = db.query(func.count()).select_from(AttendanceHistory).filter_by(user_id=user_id).scalar()
    present_days = db.query(func.count()).select_from(AttendanceHistory).filter_by(user_id=user_id, status='present').scalar()
    attendance_rate = present_days / total_days if total_days > 0 else 0.0

    personal = db.query(PersonalData).filter_by(user_id=user_id).first()
    # Check if user has *any* completed training
    has_training = db.query(UserTraining).filter_by(user_id=user_id, completed=True).first() is not None

    # Calculate collaboration score
    collaboration_score = float(
        (perf_metric.completion_rate or 0) * (1 if has_training else 0) * attendance_rate
    )

    # === STRUCTURED INPUT ===
    struct_features = np.array([[ 
        float(payroll.base_salary),
        raises,
        appraisals,
        benefits,
        penalties,
        float(performance.performance_score),
        db.query(func.count()).select_from(UserSkill).filter_by(user_id=user_id).scalar(),
        float(training.cost_of_training),
        float(has_training),
        int(attrition.risk_class),
        int(personal.age),
        float(attendance_rate),
        db.query(func.count()).select_from(SickNote).filter_by(user_id=user_id).scalar(),
        float(sentiment_row.hours_present_per_day),
        float(sentiment_row.workstation_time),
        float(sentiment_row.meetings_attended),
        float(sentiment_row.wandering_time),
        float(sentiment_row.break_time),
        float(stress_level),
        total_num_of_interactions,
        sentiment_row.num_conflicts_involved,
        collaboration_score,
        int(personal.marital_status == "Divorced"),
        int(personal.marital_status == "Married"),
        int(personal.marital_status == "Single")
    ]], dtype=np.float32)

    # === Structured Model Prediction ===
    s_input, s_output = get_input_output_details(interpreter_struct)
    interpreter_struct.set_tensor(s_input[0]['index'], struct_features)
    interpreter_struct.invoke()
    transformer_vector = interpreter_struct.get_tensor(s_output[0]['index'])

    # === Textual Input Vector (via tokenizer + TFLite) ===
    full_text = " ".join(interaction_fields)  # Safe to join
    padded = pad_text_sequences(tokenizer, [full_text])
    t_input, t_output = get_input_output_details(interpreter_text)
    interpreter_text.set_tensor(t_input[0]['index'], np.array(padded, dtype=np.float32))
    interpreter_text.invoke()
    lstm_vector = interpreter_text.get_tensor(t_output[0]['index'])


    # === Fusion Model Prediction ===
    fusion_input_vector = np.concatenate([transformer_vector, lstm_vector], axis=1)
    f_input, f_output = get_input_output_details(interpreter_fusion)
    interpreter_fusion.set_tensor(f_input[0]['index'], fusion_input_vector)
    interpreter_fusion.invoke()
    prediction = interpreter_fusion.get_tensor(f_output[0]['index'])

    sentiment_class = int(np.argmax(prediction))

    sentiment_class = int(np.argmax(prediction))

    # === Save Result to DB ===
    existing = db.query(CurrentSentimentScore).filter_by(user_id=user_id).first()
    if existing:
        existing.sentiment_score = sentiment_class
        existing.last_updated = datetime.utcnow()
    else:
        db.add(CurrentSentimentScore(
            user_id=user_id,
            sentiment_score=sentiment_class,
            last_updated=datetime.utcnow()
        ))

    db.add(SentimentScoreHistory(
        user_id=user_id,
        sentiment_score=sentiment_class,
        predicted_at=datetime.utcnow()
    ))

    db.commit()

    return {
        "user_id": user_id,
        "sentiment_score": sentiment_class,
        "confidence_vector": prediction.tolist()[0]
    }
