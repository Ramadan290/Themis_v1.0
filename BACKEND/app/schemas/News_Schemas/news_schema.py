""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 


This file is responsible for the news including :

 1 -  The base news will output all news info
        which will be crucial in displaying news in the ui 

 2 -  News Create will just inherit all of the parent class info to create a new news post
        
 3 -  Reading News , only the id is enough as i said before we dont want a lot fo api communication for speed , and this is 
       mostly for comments , i have an idea of linking them creatively wihtout loading too much on the api and affecting performance

"""

from pydantic import BaseModel ,validator
from typing import Optional
from datetime import datetime
from app.core.utils import format_datetime

class NewsBase(BaseModel):
    news_uid: Optional[str] = None  
    title: Optional[str] = None
    content: Optional[str] = None
    posted_at: Optional[str] = None  # will be formatted into str
    author: Optional[str] = None

    @validator("posted_at", pre=True)
    def format_posted_at(cls, value):
        if isinstance(value, datetime):
            return format_datetime(value)
        return value

class NewsCreate(NewsBase):
    pass # inherit all

class NewsRead(NewsBase):
    id: int

    class Config:
        from_attributes = True