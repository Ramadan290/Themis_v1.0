""""

This is the Base engine , i seperated it so i can improve the session 
speed as we dont need to bind each time the api references the database we can just bind once at runtime
then keep calling the base engine without binding again .
 
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
