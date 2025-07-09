import numpy as np
import tensorflow as tf
from sqlalchemy.orm import Session

from app.models.Prediction_Models_Models.benefit_to_cost_ratio.benefit_to_cost_ratio_history import BenefitCostRatioHistory
from app.models.Prediction_Models_Models.benefit_to_cost_ratio.current_benefit_to_cost_ratio import CurrentBCRPrediction
from app.models.Training_and_Skills_Models.user_training_model import UserTraining
from app.models.User_Models.performance_metrics_model import PerformanceMetric
from app.models.Payroll_Models.appraisals_model import Appraisal
from app.models.Payroll_Models.raise_request_model import RaiseRequest
from app.models.Payroll_Models.benefits_model import Benefit
from app.models.Payroll_Models.payroll_fixed_model import PayrollFixed
from app.models.Prediction_Models_Models.performance_prediction.current_performance_prediction import CurrentPerformancePrediction
from app.core.utils import suppress_tf_lite_logs , suppress_stderr


def predict_bcr(user_id: int, db: Session):

    with suppress_stderr():
        interpreter = tf.lite.Interpreter(
            model_path="app/prediction_models/benefit_to_cost_ratio.tflite",
            experimental_delegates=[]  # This avoids XNNPACK
        )
        interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    training = db.query(UserTraining).filter_by(user_id=user_id).first()

    # NEW: Dynamically calculate has_training
    has_training = db.query(UserTraining).filter_by(user_id=user_id, completed=True).first() is not None
    payroll = db.query(PayrollFixed).filter_by(user_id=user_id).first()
    appraisals = db.query(Appraisal).filter_by(user_id=user_id).count()
    perf_metric =  db.query(PerformanceMetric).filter_by(user_id=user_id).first()
    raises = db.query(RaiseRequest).filter_by(user_id=user_id).count()
    benefits = db.query(Benefit).filter_by(user_id=user_id).count()
    performance = db.query(CurrentPerformancePrediction).filter_by(user_id=user_id).first()

    if not (training and payroll and performance):
        return {"error": f"Missing required inputs for user {user_id}"}

    input_vector = np.array([[
        float(payroll.base_salary),
        appraisals,
        benefits,
        raises,
        perf_metric.completion_rate,
        performance.performance_score,
        float(has_training),
        training.cost_of_training
    ]], dtype=np.float32)

    interpreter.set_tensor(input_details[0]['index'], input_vector)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index']).copy()

    score = round(float(output[0][0]), 3)
    score = min(1.0, max(0.0, score))

    # Save current + history
    existing = db.query(CurrentBCRPrediction).filter_by(user_id=user_id).first()
    if existing:
        existing.bcr_score = score
    else:
        db.add(CurrentBCRPrediction(user_id=user_id, bcr_score=score))

    db.add(BenefitCostRatioHistory(user_id=user_id, bcr_score=score))
    db.commit()

    return {"user_id": user_id, "bcr_score": score}
