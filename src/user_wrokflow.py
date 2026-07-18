import jwt
from app.schema import User as User_model
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException, status
from app.database.config import get_db
from app.database.models import Users as User_database
import logging
from src.password_token import hash_password,create_access_token,verify_pass
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


Algorthim="HS256"




def get_user_data_sign(data:User_model,db:Session=Depends(get_db)):
    try:
        if db.query(User_database).filter(User_database.email==data.email).first():
            return {"Message": "User is already exit"}
    
        else:
            new_user=User_database(
                Username=data.Username,
                email=data.email,
                password=hash_password(data.password)
                )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logging.info("add new_user is done")
            
            
    except Exception as e:
        logging.error("we have error in (get_user_data)",e)


def login_user(data_form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(User_database).filter(data_form.username==User_database.email).first()

    if user and verify_pass(data_form.password,user.password):
        token=create_access_token(data={"sub":user.email})
        return{"access_token":token,
               "token_type":"bearer"}
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail="Ivalid email or password")
    
    