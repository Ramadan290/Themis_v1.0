"""
This file handles session creation and retries for a shared-memory-based SQL Server connection.
"""

import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.config import DATABASE_URL

MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

def create_stable_engine(url):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            engine = create_engine(url, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Successfully connected to the database.")
            return engine
        except OperationalError as e:
            print(f"❌ DB Connection failed (attempt {attempt}): {e}")
            time.sleep(RETRY_DELAY)
    print("🛑 All attempts to connect to the database have failed.")
    return None

engine = create_stable_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

def get_db():
    if SessionLocal is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is currently unavailable. Please try again later."
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
