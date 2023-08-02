## 0802 빅데이터를 지탱하는 기술 

### 다룬 내용
- 네트워크 기초
- FastAPI 기초 사용법 
- Model Pipeline 을 API 형태로 설계하기 

### 파일 설명 
- `books1.py` : GET, PUT, DELETE, POST 에 대한 기초
- `books2.py` : Pydantic, HTTPException 에 대한 설명 
- `api.py` : Sentiment analysis model 에 대한 api 설계
- `main.py` : Sentiment analysis model 실행
- `model` : [HuggingFace 의 sentiment analysis 모델](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion)

### uvicorn 서버 실행 방법
- uvicorn books1:app --reload
- uvicorn books2:app --reload
- uvicorn api:app --reload