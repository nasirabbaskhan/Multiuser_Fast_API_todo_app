from datetime import timedelta
from fastapi import FastAPI ,Depends, HTTPException, status
import uvicorn 
from sqlmodel import  Session, select
from todo import setting
from typing import Annotated
from contextlib import asynccontextmanager
from todo.db import create_tables, get_session
from todo.model import MultiUserTodo , Todo_Create, Todo_Edit, Token, User
from todo.router.user import user_router
from fastapi.security import OAuth2PasswordRequestForm
from todo.auth import EXPIRY_TIME, authenticate_user, create_access_token, create_refresh_token, current_user, validate_refresh_token

        
 #8 this function run firstly after app runs   
@asynccontextmanager              
async def lifespan(app:FastAPI):
    print("creating tables")
    create_tables()
    print("tabl create")
    yield
    
    
# fast api application
app:FastAPI= FastAPI(lifespan=lifespan, title="Todo app", version ="1.0.0")


# add the user authentication routs in main file from user.py file
app.include_router(router=user_router)


#9 creating end points
@app.get("/")
async def getsomeone():
    return {"message":"Welcome to our Multi User Fast API App"}


#login
# form_data will be varified by OAuth2PasswordRequestForm dependency
@app.post("/token", response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], 
                session:Annotated[Session, Depends(get_session)]):
    user = authenticate_user( form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    expire_time= timedelta(milliseconds=EXPIRY_TIME)
    access_token= create_access_token({"sub":form_data.username}, expire_time)
    
    refresh_expire_time= timedelta(days=7)
    refresh_token= create_refresh_token({"sub":user.email},refresh_expire_time)
    
    return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)
    
       
@app.post("/token/refresh")
async def refresh_token(old_refresh_token:str, session:Annotated[Session, Depends(get_session)]):
     credential_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token, Please login again",
        headers={"www-Authenticate":"Bearer"}
    )
     user = validate_refresh_token(old_refresh_token,session)
     if not user:
         raise credential_exception
     expire_time= timedelta(milliseconds=EXPIRY_TIME)
     access_token= create_access_token({"sub":user.username}, expire_time)
     
     refresh_expire_time= timedelta(days=7)
     refresh_token= create_refresh_token({"sub":user.email},refresh_expire_time)
     
     return Token(access_token=access_token, token_type="bearer", refresh_token=refresh_token)
 
 
 
 

@app.post("/todos/",response_model=MultiUserTodo )
async def create_todos(current_user:Annotated[User, Depends(current_user)],
                       todo:Todo_Create, session:Annotated[Session, 
                                                    Depends(get_session)] ):
    new_todo = MultiUserTodo (content=todo.content,user_id=current_user.id)
    # new_data= MultiUserTodo.model_validate(current_user)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo
    

@app.get("/todos/",response_model=list[MultiUserTodo])
async def get_all_todos(current_user:Annotated[User, Depends(current_user)],
                        session:Annotated[Session, Depends(get_session)]):
   
    todos= session.exec(select(MultiUserTodo ).where(MultiUserTodo .user_id==current_user.id)).all()
    return todos
    
    
@app.get("/todos/{id}")
async def get_single_todo(id:int,
                          current_user:Annotated[User, Depends(current_user)],
                          session:Annotated[Session, Depends(get_session)]):
    user_todos= session.exec(select(MultiUserTodo ).where(MultiUserTodo .user_id==current_user.id)).all()
    matched_tod= next((todo for todo in user_todos if todo.id==id),None)
    if matched_tod:
        return matched_tod
    else:
        raise HTTPException(status_code=404, detail="No Task found")
        
    
   
   

@app.put("/todos/{id}")
async def edit_todo( id:int,
                    todo:Todo_Edit,
                    current_user:Annotated[User, Depends(current_user)],
                    session:Annotated[Session, Depends(get_session)]):
    user_todos= session.exec(select(MultiUserTodo ).where(MultiUserTodo .user_id==current_user.id)).all()
    existing_todo= next((todo for todo in user_todos if todo.id==id),None)
    
    if existing_todo:
        existing_todo.content= todo.content
        existing_todo.is_completed=todo.is_completed
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException (status_code=404, detail="No task found")
         
        

@app.delete("/todos/{id}")
async def delete_todos(id:int,
                       current_user:Annotated[User, Depends(current_user)],
                       session:Annotated[Session, Depends(get_session)]):
    user_todos= session.exec(select(MultiUserTodo ).where(MultiUserTodo .user_id==current_user.id)).all() # it will return array so we have nedd to run the loop
    todo= next((todo for todo in user_todos if todo.id==id),None)
    if todo:
        session.delete(todo)
        session.commit()
        # session.refresh(todo)
        return {"message":"Task successfully Deleted!"}
    else:
        raise HTTPException (status_code=404, detail="No task found")



# function to start the server   
def start():
    uvicorn.run("todo.main:app",host="0.0.0.0", port=8000, reload=True)