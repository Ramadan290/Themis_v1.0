""""

This file will include:
  - helper functions used for hashing passwords and sensitive information 
  - verifying hash passwords against plain passwords 

  Those two functions are built in from bcrypt the foundation behind them is far more complex

"""


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
