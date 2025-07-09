""""

Access Tokens acts as the ticket for user this token will hold all user info that will then be used in his actions 

 This file includes :
  - Creating a new acess token (at login)
  - Refreshing token every 30 minutes in order to let user use the system without having to login again 
      every 30 minutes while ensuring a changeable token that will ensure security
  - decoding token is a security measure that can be used to make the acess token stronger against brute force attacks (this project is an academic simualation not intended for real use 
       so decoding may not be used )
"""



from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.settings import settings

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
