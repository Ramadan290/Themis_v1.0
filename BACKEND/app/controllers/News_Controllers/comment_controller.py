""""
Controllers are responsible for the application logic that is sent to routes and proccessed at request .

A future enhancement would be to implement services and seperate business logic but this is not necessary 
right now we dont have that many features so eveyrthing can be handled in controllers.

This file includes : 
 - Adding a Comment on a News Post (All)
 - Deleting a Comment from a News Post (Admin or oneself)

"""

from sqlalchemy.orm import Session , joinedload
from datetime import datetime
from fastapi import HTTPException
from app.models.User_Models.user_model import User
from app.models.News_Models.comment_model import Comment
from app.schemas.News_Schemas.comment_schema import CommentCreate , CommentRead
from app.core.utils import format_datetime
from app.core.utils import generate_readable_user_id, format_datetime

def post_comment(db: Session, comment_data: CommentCreate):
    new_comment = Comment(
        news_id=comment_data.news_id,
        user_id=comment_data.user_id,
        content=comment_data.content,
        commented_at=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    user = db.query(User).filter(User.id == new_comment.user_id).first()  # fetch user for username + role

    return {
        "id": new_comment.id,
        "news_id": new_comment.news_id,
        "user_id": new_comment.user_id,
        "username": user.username,  
        "content": new_comment.content,
        "commented_at": format_datetime(new_comment.commented_at),
        "author_id": generate_readable_user_id(user.id, user.role)  
    }


def get_comments_by_news(db: Session, news_id: int):
    comments = (
        db.query(Comment)
        .options(joinedload(Comment.user))
        .filter(Comment.news_id == news_id)
        .order_by(Comment.commented_at.desc())
        .all()
    )

    return [
        CommentRead(
            id=c.id,
            news_id=c.news_id,
            user_id=c.user_id,
            username=c.user.username,
            content=c.content,
            commented_at=c.commented_at
        )
        for c in comments
    ]

def delete_comment(db: Session, comment_id: int, current_user):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Allow delete if user is admin or the owner of the comment
    if current_user.role != "admin" and current_user.id != comment.user_id:
        raise HTTPException(status_code=403, detail="Permission denied")

    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted successfully"}
