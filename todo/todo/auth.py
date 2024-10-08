from passlib.context import CryptContext 
from typing import Annotated
from todo.db import get_session
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from todo.model import User, MultiUserTodo , refreshTokenData, tokenData
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError 
from datetime import datetime, timedelta, timezone

outh_sheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context= CryptContext(schemes="bcrypt")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password,hash_password):
    return pwd_context.verify(password, hash_password)

def get_user_from_db(session:Annotated[Session,Depends(get_session) ],
                     email:str|None= None,
                     username:str | None= None):
    statement= select(User).where(User.username==username)
    user = session.exec(statement).first()
    return user
    
    
def authenticate_user(username,password, session:Annotated[Session, Depends(get_session)]):
    db_user= get_user_from_db(session, username=username)
    if not db_user:
        return False
    if not verify_password(password=password, hash_password=db_user.password):
        return False
    return db_user

# to create the access token function
SECRET = 'secret'
ALGORITHEM = "HS256"
EXPIRY_TIME= 1

def create_access_token(data:dict, expiry_time:timedelta| None):
    data_to_encode= data.copy()
    # if expiry_time:
    #      expire = datetime.now(timezone.utc) + expiry_time
    # else:
    #     expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # data_to_encode.update({"exp": expire})
    encoded_jwt= jwt.encode(data_to_encode, SECRET, algorithm = ALGORITHEM )
    return encoded_jwt
             
             
def current_user(token:Annotated[str, Depends(outh_sheme)], session:Annotated[Session, Depends(get_session)]):
    print("now token",token)
    credential_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token, Please login again",
        headers={"www-Authenticate":"Bearer"}
    )
    
    try:
        
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHEM])
     
        username:str | None = payload.get("sub")
        if username is None:
            raise credential_exception
        token_tada= tokenData(username=username)
    except:
        print("we are incorect")
        raise JWTError
    user = get_user_from_db(session, username=token_tada.username)
    if not user:
        raise credential_exception
    return user


    
  
#refresh access token
def create_refresh_token(data:dict, expiry_time:timedelta| None):
    data_to_encode= data.copy()
    if expiry_time:
         expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt= jwt.encode(data_to_encode, SECRET, algorithm = ALGORITHEM )
    return encoded_jwt




def validate_refresh_token(token:str,
                           session:Annotated[Session, Depends(get_session)]):
    credential_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token, Please login again",
        headers={"www-Authenticate":"Bearer"}
    )
    
    try:
        
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHEM])
        
        email:str | None = payload.get("sub")
        if email is None:
            raise credential_exception
        token_tada= refreshTokenData(email=email)
    except:
       
        raise JWTError
    user = get_user_from_db(session, email=token_tada.email)
    if not user:
        raise credential_exception
    return user