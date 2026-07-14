import os
import json
import sys
import torch
import logging
from fastapi import FastAPI, HTTPException
from transformers import DistilBertTokenizerFast, AutoModelForSequenceClassification
from contextlib import asynccontextmanager
from src.config import Settings
from app.routers.model import router_predict
from app.routers.auth import router_auth
from app.database import models
from app.database.config import engine

s=Settings()
MODEL_DIR=s.model_url

@asynccontextmanager
async def lifeSpam(app:FastAPI):
    try:
        app.state.tokenizer=DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
        logging.info("load tokenizer is done")
        app.state.model=AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        logging.info("load model is done")
        app.state.model.eval()
    except Exception as e:
        logging.error("we have error in load model and tokenizer")
        sys.exit(1)
    yield
    
models.Base.metadata.create_all(bind=engine)
app=FastAPI(lifespan=lifeSpam)

app.include_router(router_predict)
app.include_router(router_auth)

   
