from pydantic import BaseModel
from sqlmodel import SQLModel, Field 
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm 
from typing import Annotated


#4: create the model
 # data model (data validation using pydantic model)
 # table model (table creation)
class MultiUserTodo (SQLModel, table=True):
    id:int | None= Field(default=None, primary_key=True)
    content: str = Field(index=True, min_length=4, max_length=50)
    is_completed : bool = Field(default=False)
    user_id :int= Field(foreign_key="user.id")
    
class User (SQLModel, table = True):
    id: int = Field(default=None , primary_key=True)
    username:str
    email:str
    password:str
    


  
 # it is dependency class using valdation of user registration   
class Register_user(BaseModel):
    username: Annotated[
        str,
        Form() 
    ]
    email: Annotated[
        str,
        Form() 
    ]
    password: Annotated[
        str,
        Form() 
    ]
        
        
class Token(BaseModel):
    access_token:str
    token_type:str
    refresh_token:str | None = None
    
class tokenData(BaseModel):
    username:str
    
    
class Todo_Create (BaseModel):
    content: str = Field(index=True, min_length=4, max_length=50)
    
    
class Todo_Edit(BaseModel):
     content: str 
     is_completed : bool
     
class refreshTokenData(BaseModel):
    email:str