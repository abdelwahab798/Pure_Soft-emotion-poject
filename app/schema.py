from pydantic import BaseModel,EmailStr


class Request(BaseModel):
    text:str


class Response(BaseModel):
    text:str
    Predict:str
    confidence:float
    


class User(BaseModel):
    Username:str
    email:EmailStr
    password:str

class Tokens(BaseModel):
    access_token:str
    token_type:str


class_Names=["sadness","joy","love","anger","fear","surprise"]