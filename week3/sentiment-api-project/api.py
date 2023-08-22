from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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

class SentimentRequest(BaseModel):
    text : str = ""
    class Config:
        schema_extra = {
            'example': {
            'text' : 'Put in text to sentiment analysis'
            }
        }


class SentimentResult(BaseModel):
    sentence : str = ""
    label_1 : str = ""
    score_1 : float = ""
    label_2 : str = ""
    score_2 : float = ""

@app.post('/sentiment')
async def root(payload: SentimentRequest):
    if len(payload.text) <= 3:
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
    
    