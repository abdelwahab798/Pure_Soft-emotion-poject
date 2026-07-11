import os
import json
import sys
import torch
import logging
from fastapi import FastAPI, HTTPException
from transformers import DistilBertTokenizerFast, AutoModelForSequenceClassification
from contextlib import asynccontextmanager
from app.schema import Response , Request,class_Names
from src.config import Settings

s=Settings()
MODEL_DIR=s.model_url

@asynccontextmanager
async def lifeSpam(app:FastAPI):
    global tokenizer,model
    try:
        tokenizer=DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
        logging.info("load tokenizer is done")
        model=AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        logging.info("load model is done")
        model.eval()
    except Exception as e:
        logging.error("we have error in load model and tokenizer")
        sys.exit(1)
    yield
    
app=FastAPI(lifespan=lifeSpam)



   
@app.post("/predict",response_model=Response)
async def predict(request:Request):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty.")
    try:
        input=tokenizer(
            request.text,
            return_tensors="pt",
            truncation=True
        )

        with torch.no_grad():
            output=model(**input)
            probs=torch.softmax(output.logits,dim=1)
            predict=probs.argmax(dim=1).item()
            confidence = probs[0][predict].item()
            predict_str=class_Names[predict]

        return Response(
                Predict=predict_str,
                confidence=confidence
            )
        
    except Exception as e:
        print("prediction error")
        raise HTTPException(status_code=500, detail=str(e))
