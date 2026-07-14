from sqlalchemy import Column , String , Integer,ForeignKey,Float
from app.database.config import Base

class Users(Base):
    __tablename__="users"
    Username=Column(String,index=True)
    email=Column(String,unique=True,index=True,primary_key=True)
    password=Column(String)


class Text(Base):
    __tablename__="Predictions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_email=Column(String,ForeignKey("users.email"))
    Text=Column(String)
    Prediction=Column(String)
    confidence=Column(Float)
    