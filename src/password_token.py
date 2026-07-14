import bcrypt
import logging
from src.config import Settings
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException, status


s=Settings()
SECRET_KEY=s.SECRET_KEY
Algorthim="HS256"

Oauth=OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data:dict):
    encode=data.copy()
    return jwt.encode(encode,SECRET_KEY,Algorthim)


def get_user_access(token:str=Depends(Oauth)):
    try:
        print("DEBUG token received:", repr(token))
        exc=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",)
        p =jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email:str=p.get("sub")
        if email is None:
            raise exc
        return email
    except Exception as e:
        logging.error("we have error in (get_user_access: %s",e)
        raise exc




def hash_password(password:str)->str:
    try:
        password=password.encode("utf-8")
        s=bcrypt.gensalt()
        password=bcrypt.hashpw(password,s)
        logging.info("hash password is done")
        return password.decode("utf-8")
    except Exception as e:
        logging.error("we have error in (hash_password)",e)
        raise e



def verify_pass(input_pass:str,exit_pass:str):
    try:
        input_pass=input_pass.encode("utf-8")
        exit_pass=exit_pass.strip().encode("utf-8")
        logging.info("check password is done")
        return bcrypt.checkpw(input_pass,exit_pass)
    except Exception as e:
        logging.error("we have error in (verify_pass)",e)
        raise e


    

