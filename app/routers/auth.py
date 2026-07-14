from fastapi import APIRouter
from app.schema import Tokens
from src.user_wrokflow import get_user_data_sign,login_user
from app.schema import User as User_model
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.config import get_db
from fastapi.security import OAuth2PasswordRequestForm


router_auth =APIRouter()



@router_auth.post("/sign")
def load_sign(data:User_model,db:Session=Depends(get_db)):
    get_user_data_sign(data,db)


@router_auth.post("/login",response_model=Tokens)
def load_login(data_form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return login_user(data_form,db)
