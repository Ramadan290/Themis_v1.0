"""
This schema file handles all comment-related input/output models.

- CommentBase: base structure shared by Create/Read
- CommentCreate: used for creating new comments
- CommentIn: used for frontend input (excludes user_id)
- CommentRead: used for sending comments to frontend with username
"""

from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from app.core.utils import format_datetime


# Shared fields
class CommentBase(BaseModel):
    news_id: int
    user_id: int
    content: Optional[str] = None


# Used for inserting a comment
class CommentCreate(CommentBase):
    pass


# Used for receiving comment from UI (no user_id since it's from token)
class CommentIn(BaseModel):
    news_id: int
    content: Optional[str] = None


# Used for sending comment to frontend
class CommentRead(BaseModel):
    id: int
    news_id: int
    user_id: int
    username: str
    content: Optional[str] = None
    commented_at: Optional[str] = None  # formatted as string (not datetime)

    @validator("commented_at", pre=True)
    def format_commented_at(cls, value):
        if isinstance(value, datetime):
            return format_datetime(value)  # your utility formatting function
        return value

    class Config:
        from_attributes = True
