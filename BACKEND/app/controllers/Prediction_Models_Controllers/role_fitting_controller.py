from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import numpy as np
import tensorflow as tf
from collections import defaultdict

from app.models.User_Models.user_model import User
from app.models.Training_and_Skills_Models.user_skills_model import UserSkill
from app.models.Training_and_Skills_Models.skills_model import Skill
from app.models.Training_and_Skills_Models.departments_model import Department
from app.models.Training_and_Skills_Models.deparments_skill_model import department_skills
from app.models.User_Models.performance_metrics_model import PerformanceMetric
from app.models.Prediction_Models_Models.performance_prediction.current_performance_prediction import CurrentPerformancePrediction


def map_user_id_to_index(user_id: int, db: Session) -> int:
    all_user_ids = db.query(User.id).order_by(User.id).all()
    id_list = [uid[0] for uid in all_user_ids]

    if user_id not in id_list:
        raise HTTPException(status_code=404, detail="User ID not found in system.")

    return id_list.index(user_id)


def predict_fit_score(user_id: int, db: Session):
    # === Step 0: Load TFLite model ===
    interpreter = tf.lite.Interpreter(model_path="app/prediction_models/role_fitting.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # === Step 1: Get user and department ===
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.department_id:
        raise HTTPException(status_code=404, detail="User or department not found")
    department_id = user.department_id

    # === Step 2: Build skill vector ===
    all_skills = db.query(Skill).order_by(Skill.id).all()
    skill_id_to_index = {skill.id: idx for idx, skill in enumerate(all_skills)}
    skill_vector = np.zeros(len(skill_id_to_index), dtype=np.float32)

    user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
    user_skill_ids = {s.skill_id for s in user_skills}

    for skill_id in user_skill_ids:
        if skill_id in skill_id_to_index:
            skill_vector[skill_id_to_index[skill_id]] = 1.0

    # === Step 3: Fetch performance metrics ===
    metrics = db.query(PerformanceMetric).filter(PerformanceMetric.user_id == user_id).first()
    if not metrics:
        raise HTTPException(status_code=404, detail="Performance metrics not found for user")
    completion_rate = np.array([[metrics.completion_rate]], dtype=np.float32)

    # === Step 4: Fetch efficiency score ===
    score = db.query(CurrentPerformancePrediction).filter(CurrentPerformancePrediction.user_id == user_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Current performance score not found for user")
    efficiency_score = np.array([[score.performance_score]], dtype=np.float32)

    user_index = map_user_id_to_index(user_id, db)

    # === Step 5: Set TFLite model inputs ===
    interpreter.set_tensor(input_details[0]["index"], skill_vector[:37].reshape(1, -1))
    interpreter.set_tensor(input_details[1]["index"], np.array([[user_index]], dtype=np.float32))
    interpreter.set_tensor(input_details[2]["index"], np.array([[float(department_id)]], dtype=np.float32))
    interpreter.set_tensor(input_details[3]["index"], completion_rate)
    interpreter.set_tensor(input_details[4]["index"], efficiency_score)

    # === Step 6: Run Prediction ===
    interpreter.invoke()
    fit_score = float(interpreter.get_tensor(output_details[0]["index"])[0][0])

    # === Step 7: Decision Logic ===
    if fit_score >= 0.60:
        return {
            "fit_score": fit_score,
            "decision": "Stay in current department",
            "message": "Your fit score is good. Keep up the great work!"
        }

    elif 0.55 <= fit_score < 0.60:
        result = db.execute(select(department_skills.c.skill_id).where(department_skills.c.department_id == department_id))
        dept_skill_ids = [row[0] for row in result]
        required_skills = set(dept_skill_ids)

        missing_skills = db.query(Skill).filter(Skill.id.in_(required_skills - user_skill_ids)).all()
        missing_names = [s.name for s in missing_skills]

        return {
            "fit_score": fit_score,
            "decision": "Moderate fit — Training Recommended",
            "missing_skills": missing_names,
            "message": "You're close to a great fit! Some targeted training can help you improve."
        }

    elif 0.50 <= fit_score < 0.55:
        result = db.execute(select(department_skills.c.skill_id).where(department_skills.c.department_id == department_id))
        dept_skill_ids = [row[0] for row in result]
        required_skills = set(dept_skill_ids)

        missing_skills = db.query(Skill).filter(Skill.id.in_(required_skills - user_skill_ids)).all()
        missing_names = [s.name for s in missing_skills]

        return {
            "fit_score": fit_score,
            "decision": "Low fit — Training Strongly Recommended",
            "missing_skills": missing_names,
            "message": "Your fit score indicates room for improvement. We recommend focused training."
        }

    else:
        # === Suggest Department Transfer ===
        departments = db.query(Department).all()
        dept_skill_map = defaultdict(set)

        for dept in departments:
            skill_rows = db.execute(
                select(department_skills.c.skill_id).where(department_skills.c.department_id == dept.id)
            ).fetchall()
            skill_ids = [row[0] for row in skill_rows]
            dept_skill_map[dept.id] = set(skill_ids)

        best_dept_id = None
        best_fit_ratio = 0.0

        for dept_id, required_skills in dept_skill_map.items():
            if not required_skills:
                continue
            matched = len(user_skill_ids & required_skills)
            total = len(required_skills)
            ratio = matched / total
            if ratio > best_fit_ratio:
                best_fit_ratio = ratio
                best_dept_id = dept_id

        if not best_dept_id:
            return {
                "fit_score": fit_score,
                "decision": "Suggest department transfer",
                "message": "No suitable department match found based on your current skills."
            }

        best_dept = db.query(Department).filter(Department.id == best_dept_id).first()
        missing_ids = dept_skill_map[best_dept_id] - user_skill_ids
        missing_skills = db.query(Skill).filter(Skill.id.in_(missing_ids)).all()
        missing_names = [s.name for s in missing_skills]

        return {
            "fit_score": fit_score,
            "decision": "Suggest department transfer",
            "suggested_department": best_dept.name,
            "fit_percent": round(best_fit_ratio, 2),
            "missing_skills": missing_names,
            "message": f"Your skillset fits better in the {best_dept.name} department. Consider a transfer."
        }
