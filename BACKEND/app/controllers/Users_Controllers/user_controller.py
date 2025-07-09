""""
Controllers are responsible for the application logic that is sent to routes and proccessed at request .

A future enhancement would be to implement services and seperate business logic but this is not necessary 
right now we dont have that many features so eveyrthing can be handled in controllers.

This file includes : 
 - User Creation (Admin & HR)
 - User Login (All)

"""
from sqlalchemy import text 
from sqlalchemy.orm import Session , joinedload
from fastapi import HTTPException, status
from app.models.User_Models.user_model import User
from app.schemas.User_Schemas.user_schema import UserCreate, UserLogin
from app.core.security import verify_password , hash_password
from app.core.auth import create_access_token , create_refresh_token
from app.core.utils import generate_readable_user_id
from app.models.Training_and_Skills_Models.departments_model import Department



# User Creation
def create_user(db: Session, user_data: UserCreate):
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_pw,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    readable_id = generate_readable_user_id(new_user.id , new_user.role)
    return {"id": readable_id, "username": new_user.username, "role": new_user.role}


def login_user(db: Session, login_data: UserLogin):
    print("Login payload:", login_data)

    # Connection ping (resolves stale connection or cold start)
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        print("Database ping failed during login:", e)
        raise HTTPException(status_code=500, detail="Database connection error")

    # User verification
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Token generation
    access_token = create_access_token(data={
        "sub": user.username,
        "id": user.id,
        "role": user.role
    })

    refresh_token = create_refresh_token(data={
        "sub": user.username
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role
    }



def get_all_users(db: Session):
    return db.query(User).all()


def get_all_users_with_departments(db: Session):
    users = db.query(User).options(joinedload(User.department)).all()
    results = []
    for user in users:
        results.append({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "department": user.department.name if user.department else None
        })
    return results