
from fastapi import APIRouter,Request as FastAPIRequest
from app.schema import Response,Request
from src.predict import predict_text
from sqlalchemy.orm import Session
from app.database.config import get_db
from fastapi import Depends
from src.password_token import get_user_access
from app.database.models import Text as Text_database



router_predict=APIRouter()


@router_predict.post("/predict",response_model=Response)
def predict(text:Request,request:FastAPIRequest,db:Session=Depends(get_db),user_email:str=Depends(get_user_access)):
    tokenizer=request.app.state.tokenizer
    model=request.app.state.model
    response=predict_text(text,tokenizer,model)
    
    history=Text_database(
        user_email=user_email,
        Text=text.text,
        Prediction=response.Predict,
        confidence=response.confidence
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return response



    



