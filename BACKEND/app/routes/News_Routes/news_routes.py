"""
Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - Posting a News Post (Admin & HR)
 - Deleting a News Post (Admin & HR)

"""


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, require_role
from app.controllers.News_Controllers import news_controller
from app.schemas.News_Schemas.news_schema import NewsCreate, NewsRead
from typing import List

router = APIRouter(prefix="/news", tags=["News"])




# Fetch All News
@router.get("/all", response_model=List[NewsRead], summary="Get all news posts (Open to all)")
def get_all_news(
    db: Session = Depends(get_db)
):
    return news_controller.get_all_news(db)


# News Creation
@router.post("/add", response_model=NewsRead, summary="Add a news post (Admin & HR only)")
def create_news(
    news_data: NewsCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin", "hr"]))
):
    return news_controller.add_news(db, news_data, author=current_user.username)


# News Deletion
@router.delete("/delete/{news_id}", summary="Delete a news post by ID (Admin & HR only)")
def remove_news(
    news_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role(["admin", "hr"]))
):
    return news_controller.delete_news(db, news_id)
