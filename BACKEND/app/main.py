""""
 - This is the main folder and the start point of all routes 
 - also includes the cross origin middleware
"""


from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes.User_Routes import user_routes
from app.database.session import SessionLocal
from sqlalchemy import text
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"





from app.routes.News_Routes import news_routes , comment_routes 
from app.routes.Attendance_Routes import attendance_sheet_routes
from app.routes.Attendance_Routes import attendance_history_routes
from app.routes.Attendance_Routes import sick_notes_routes
from app.routes.Payroll_Routes import payroll_fixed_routes
from app.routes.Payroll_Routes import payroll_route
from app.routes.Payroll_Routes import payroll_history_routes
from app.routes.Payroll_Routes import appraisals_routes
from app.routes.Payroll_Routes import penalty_routes
from app.routes.Payroll_Routes import benefits_catalog_routes
from app.routes.Payroll_Routes import benefits_routes
from app.routes.Payroll_Routes import raise_request_routes
from app.routes.Training_and_Skills_Routes import department_skills_route 
from app.routes.Training_and_Skills_Routes import training_courses_routes 
from app.routes.Training_and_Skills_Routes import user_skills_route 
from app.routes.Prediction_Models_Routes import performance_prediction_route
import tensorflow as tf 
from app.routes.Prediction_Models_Routes import attrition_risk_routes
from app.routes.Prediction_Models_Routes import benefit_to_cost_ratio_route
from app.routes.Prediction_Models_Routes import sentiment_score_route
from app.routes.Prediction_Models_Routes import role_fitting_routes
from app.routes.Training_and_Skills_Routes import training_route
from app.routes.User_Routes import user_status_route
from app.database.session import SessionLocal
from app.controllers.Payroll_Controllers import payroll_controller, payroll_history_controller
from app.models.Payroll_Models.payroll_model import Payroll
import random
import time
import os
import sys
from datetime import datetime
from calendar import monthrange

from app.controllers.Payroll_Controllers.payroll_history_controller import process_payroll_to_history


from datetime import datetime




app = FastAPI(title="Themis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def archive_payroll_to_history_on_startup():
    from app.database.session import SessionLocal
    from app.controllers.Payroll_Controllers import payroll_controller, payroll_history_controller
    import random, time, os, sys
    from datetime import datetime

    try:
        db = SessionLocal()

        # ✅ Step 1: Archive any existing payrolls (regardless of period)
        try:
            result = payroll_history_controller.process_payroll_to_history(db=db)
            print("[✅] Payroll archived to history:", result["message"])
        except HTTPException as e:
            print(f"[⏭️] Archive skipped: {e.detail}")

        # ✅ Step 2: Simulate a period for new payroll sheet
        simulated_year = random.randint(2020, 2024)
        simulated_month = random.randint(1, 12)
        period = f"{simulated_year}-{simulated_month:02d}"
        print(f"[📅] Simulated Payroll Period: {period}")

        # ✅ Step 3: Generate payroll for this period
        print("[🛠️] Generating new payroll sheet...")
        sheet_result = payroll_controller.create_payroll_sheet(db=db, period=period)
        print(f"[✅] Payroll sheet generation complete: {sheet_result['message']}")

    except Exception as e:
        err_msg = str(e)
        if "Duplicate entries" in err_msg:
            print(f"[⚠️] Archive error: {err_msg}")
        else:
            print(f"[❌] Failed during payroll processing: {err_msg}")
            print("[🔁] Restarting application in 3 seconds...")
            time.sleep(3)
            os.execv(sys.executable, [sys.executable] + sys.argv)
    finally:
        db.close()




@app.on_event("startup")
@app.on_event("startup")
def archive_if_exists_then_generate_sheet():
    from app.database.session import SessionLocal
    from app.controllers.Attendance_Controllers import attendance_history_controller, attendance_sheet_controller
    from app.models.Attendance_Models.attendance_sheet_model import AttendanceSheet
    from datetime import datetime

    try:
        db = SessionLocal()

        # ✅ Step 1: Check if there's an attendance sheet to archive
        existing_sheet = db.query(AttendanceSheet).first()
        if existing_sheet:
            attendance_history_controller.push_attendance_to_history(db)
            print("[✅] Existing attendance sheet archived to history.")
        else:
            print("[ℹ️] No attendance sheet to archive — skipping archive.")

        # ✅ Step 2: Generate new sheet
        today = datetime.utcnow().strftime("%Y-%m-%d")
        session_tag = f"{today}-AM"
        attendance_sheet_controller.generate_attendance_sheet(db=db, session_tag=session_tag)
        print(f"[✅] New attendance sheet generated with session_tag: {session_tag}")

    except Exception as e:
        print(f"[⚠️] Attendance startup process failed: {str(e)}")

    finally:
        if 'db' in locals():
            db.close()



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# Serve Fronted Files
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
frontend_path = os.path.join(BASE_DIR, "FRONTEND")

if not os.path.exists(frontend_path):
    raise RuntimeError(f"Directory '{frontend_path}' does not exist")

app.mount("/FRONTEND", StaticFiles(directory=frontend_path), name="FRONTEND")




# Redirect root to login.html
@app.get("/")
def home():
    return RedirectResponse(url="FRONTEND/auth/user_login/user_login.html")


@app.get("/ping")
async def ping():
    return {"message": "I am here and working"}



@app.get("/test-db")
def test_db():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return {"db_status": "connected"}
    except Exception as e:
        return {"db_status": "error", "details": str(e)}
    finally:
        db.close()



app.include_router(user_routes.router)
app.include_router(news_routes.router)
app.include_router(comment_routes.router)
app.include_router(attendance_sheet_routes.router)
app.include_router(attendance_history_routes.router)
app.include_router(sick_notes_routes.router)
app.include_router(payroll_fixed_routes.router)
app.include_router(payroll_route.router)
app.include_router(payroll_history_routes.router)
app.include_router(appraisals_routes.router)
app.include_router(penalty_routes.router)
app.include_router(benefits_routes.router)
app.include_router(benefits_catalog_routes.router)
app.include_router(raise_request_routes.router)
app.include_router(department_skills_route.router)
app.include_router(user_skills_route.router)
app.include_router(training_courses_routes.router)


app.include_router(training_route.router)
app.include_router(user_status_route.router)


app.include_router(performance_prediction_route.router)
app.include_router(attrition_risk_routes.router)
app.include_router(benefit_to_cost_ratio_route.router)
app.include_router(sentiment_score_route.router)
app.include_router(role_fitting_routes.router)


