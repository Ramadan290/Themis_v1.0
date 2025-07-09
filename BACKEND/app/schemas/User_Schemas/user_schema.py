""""

This schemas are responsible for how data is sent to the API and received from it.
It also verifies input and output , more of validation

orm_mode = true , allows pydantic schemes to access fields via attributes instead of dict keys which would be a hassle 



This file is responsible for the users including :

 1 -  The user base which will output the username and role 
       (this is the only exception class in which we will not output everything as there is sensitive info here )

 2 -  User Create will only need the password as we will be generating most of the other things in user read and user out
        
 3 -  User login is for linking user to everyhting if i call user base everytime i will degrade 
      performance thats why i am creating another pydantic scheme

 4 - User out outputs the info needed as complmenetary for base which we will use to display users to admin and to user exclusively and hr ofcoures
  

"""


from pydantic import BaseModel
from typing import Literal ,Optional

class UserBase(BaseModel):
    username: str
    role: Literal["employee", "hr", "admin"]

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username : str
    password : str

class UserWithDepartment(BaseModel):
    id: int
    username: str
    role: str
    department: Optional[str]  # this will hold department.name

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True
