from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Results(Base):
    __tablename__ = 'Text_Sentiment_Results'
    
    id = Column(Integer, primary_key=True,index=True)
    sentence = Column(String)
    label_1 = Column(String)
    score_1 = Column(Integer)
    label_2 = Column(String)
    score_2 = Column(Integer)
    
    