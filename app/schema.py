from pydantic import BaseModel


class Request(BaseModel):
    text:str


class Response(BaseModel):
    Predict:str
    confidence:float


class_Names=["sadness","joy","love","anger","fear","surprise"]