"""
Routes are the actual links that redirect user based on current page and action ,
 and this is where we call our controllers to handle the logic and get back to us with the data required

 
This File includes : 
 - Posting a comment on a news Post (All)
 - Deleting a comment from a News Post (Admin & oneself)

"""


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.News_Schemas.comment_schema import CommentCreate, CommentRead , CommentIn
from app.controllers.News_Controllers import comment_controller
from app.core.dependencies import get_db, get_current_user
from typing import List


router = APIRouter(prefix="/comment", tags=["Comments"])




@router.get("/news/{news_id}", response_model=List[CommentRead], summary="Get all comments for a specific news post")
def get_comments_by_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    return comment_controller.get_comments_by_news(db, news_id)

@router.post("/post", response_model=CommentRead)
def post_comment(
    comment_data: CommentIn, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    comment_to_create = CommentCreate(
        news_id=comment_data.news_id,
        content=comment_data.content,
        user_id=current_user.id
    )
    return comment_controller.post_comment(db, comment_to_create)


@router.delete("/delete/{comment_id}", summary="Delete a comment (Owner or Admin)")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return comment_controller.delete_comment(db, comment_id, current_user)
