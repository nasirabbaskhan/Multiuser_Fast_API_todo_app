from typing import Annotated
from fastapi import APIRouter , Depends, HTTPException
from todo.auth import current_user, get_user_from_db, hash_password, outh_sheme
from todo.model import Register_user, User
from todo.db import get_session
from sqlmodel import Session



user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses= {404: {"description": "Not found"}}
)

@user_router.get("/")
async def read_user():
    return {"message":"Welcome to Daily todo app user page"}

@user_router.get("/auth")
def auth_rout(current_user: Annotated[User, Depends(current_user)]):
    return current_user
    

@user_router.post("/register/")
async def register_user(new_user:Annotated[Register_user,Depends() ], 
                        session:Annotated[Session, Depends(get_session)]):
    db_user= get_user_from_db(session, new_user.username)
    if db_user:
        HTTPException(status_code=409, detail="user with these credentials already exists")
    user = User(username=new_user.username,
                email=new_user.email,
                password=hash_password(new_user.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f""" User with {user.username} successfully"""}
        
    