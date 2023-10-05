from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Results
from database import engine, SessionLocal
import starlette.status as status
from main import sentiment


app = FastAPI(title = "Soeun's Sentiment Analysis",
            version = "1.0")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Depends : get_db 함수에 의존한다 -> db 열고 닫기 
db_dependency = Annotated[Session, Depends(get_db)]

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

@app.get("/",status_code = status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Results).all()


@app.post('/sentiment',status_code = status.HTTP_201_CREATED)
async def create_text_sentiment(db:db_dependency,text_request:SentimentRequest):
    if len(text_request.text) <= 3:
        raise HTTPException(status_code = 201, detail = "Please put in valid text")
        
    label_1, label_2 ,score_1, score_2 = sentiment(text_request.text)
    text_result = SentimentResult(sentence = text_request.text,
                        label_1 = label_1,
                        score_1 = score_1,
                        label_2 = label_2,
                        score_2 = score_2
    )
    text_model = Results(**text_result.dict())
    
    db.add(text_model)
    db.commit()
    
@app.delete('/sentiment/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_text(db:db_dependency,id : int = Path(gt=0)):
    text_model = db.query(Results).filter(Results.id == id).first()
    if text_model is None:
        raise HTTPException(status_code = 404, detail = 'ID not found')
    db.query(Results).filter(Results.id == id).delete()
    db.commit()

