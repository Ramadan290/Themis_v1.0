""""
Controllers are responsible for the application logic that is sent to routes and proccessed at request .

A future enhancement would be to implement services and seperate business logic but this is not necessary 
right now we dont have that many features so eveyrthing can be handled in controllers.

This file includes : 
 - Adding a News Post
 - Deleting a News Post

"""

from sqlalchemy.orm import Session
from datetime import datetime
from app.models.News_Models.news_model import News
from app.schemas.News_Schemas.news_schema import NewsCreate , NewsRead
from fastapi import HTTPException
from app.models.News_Models.comment_model import Comment
from app.core.utils import generate_news_uid , format_datetime
from datetime import datetime


# Load News
def get_all_news(db: Session):
    news_list = db.query(News).order_by(News.posted_at.desc()).all()    
    return news_list


def add_news(db: Session, news_data: NewsCreate, author: str):
    new_news = News(
        news_uid=generate_news_uid(),
        title=news_data.title,
        content=news_data.content,
        posted_at = format_datetime(datetime.utcnow()),
        author=author
    )
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    
    return {
        "id": new_news.id,
        "news_uid": new_news.news_uid,
        "title": new_news.title,
        "content": new_news.content,
        "posted_at": format_datetime(new_news.posted_at), 
        "author": new_news.author
    }

def delete_news(db: Session, news_id: int):
    news_item = db.query(News).filter(News.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")

    # Delete all comments related to this news first
    db.query(Comment).filter(Comment.news_id == news_id).delete(synchronize_session=False)

    # Now delete the news
    db.delete(news_item)
    db.commit()
    return {"detail": "News deleted successfully"}