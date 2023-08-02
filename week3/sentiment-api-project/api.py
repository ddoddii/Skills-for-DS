from fastapi import FastAPI, HTTPException, APIRouter, Body
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from main import sentiment

logger = logging.getLogger(name='MyLog')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('|%(asctime)s||%(name)s||%(levelname)s|\n%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S'
                            )

stream_handler = logging.StreamHandler() 
stream_handler.setFormatter(formatter) 
logger.addHandler(stream_handler) 

app = FastAPI(title = "Soeun's Sentiment Analysis",
              version = "1.0")

class SentimentRequset(BaseModel):
    text : str = Field(min_length=3)

class SentimentResult(BaseModel):
    label_1 : str = ""
    score_1 : int = ""
    label_2 : str = ""
    score_2 : int = ""

@app.post('/sentiment')
async def root(payload: SentimentRequset):
    if len(payload.text) <= 0:
        raise HTTPException(status_code = 201, detail = "Please put in valid text")
        
    try:
        label_1, label_2 ,score_1, score_2 = sentiment(payload.text)
        return SentimentResult(sentence = payload.text,
                            label_1 = label_1,
                            score_1 = score_1,
                            label_2 = label_2,
                            score_2 = score_2
        )
    
    except Exception as e:
        logger.error("Exception:"+str(e))
        raise HTTPException(status_code = 404, detail=f"Exception Error: {e}")