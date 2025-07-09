"""
Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - User Creation (Admin & HR)
 - User Login (All)
 - Fetch current user from db session data
"""


from fastapi import APIRouter, Depends ,HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.User_Schemas.user_schema import UserCreate, UserLogin , UserOut
from app.models.User_Models.user_model import User
from app.core.dependencies import get_db, get_current_user, require_role
from app.controllers.Users_Controllers import user_controller
from app.core.utils import generate_readable_user_id
from app.models.Payroll_Models.payroll_model import Payroll
from app.schemas.User_Schemas.user_schema import UserWithDepartment
from app.core.dependencies import get_db



router = APIRouter(prefix="/auth", tags=["Users"])


# User Creation

@router.post("/create")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))  
):
    return user_controller.create_user(db, user_data)



# User Login 

@router.post("/login", summary="Login to receive access and refresh tokens")
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    return user_controller.login_user(db, login_data)


# Fetch current User

@router.get("/me", summary="Get current user info")
def get_me(current_user = Depends(get_current_user)):
    return {
        "id" : generate_readable_user_id(current_user.id , current_user.role) , 
        "username": current_user.username,
        "role": current_user.role
    }


@router.get("/all", response_model=List[UserOut], summary="Get all user accounts (Admin only)")
def get_all_users(
    db: Session = Depends(get_db),
    _ = Depends(require_role(["hr"]))
):
    return user_controller.get_all_users(db)


@router.get("/users/by-username/{username}")
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/by-id/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




@router.get("/with-department", response_model=List[UserWithDepartment], summary="Get all users with department names")
def get_users_with_departments(
    db: Session = Depends(get_db),
    _ = Depends(require_role(["hr"]))
):
    return user_controller.get_all_users_with_departments(db)