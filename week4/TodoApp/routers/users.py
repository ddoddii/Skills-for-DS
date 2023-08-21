from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Users
from database import SessionLocal
import starlette.status as status
from .auth import get_current_user

router = APIRouter(
    prefix = '/users',
    tags = ['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#* Depends : get_db 함수에 의존한다 -> db 열고 닫기 
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserRequest(BaseModel):
    email : str
    username : str
    first_name : str
    last_name : str
    password : str = Field(min_length = 3, max_length = 20)
    role : str

@router.get('/get_user',status_code = status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code = 401, detail = "Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).all()

@router.put('/change_password',status_code = status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency,
                          user_request : UserRequest,
                          user_id : int):
    if user is None:
        raise HTTPException(status_code = 401, detail = 'Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user_id).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code = 404, detail = 'User not found')
    
    user_model.email = user_request.email
    user_model.username = user_request.username
    user_model.first_name = user_request.first_name
    user_model.last_name = user_request.last_name
    user_model.password = user_request.password
    user_model.role = user_request.role
    
    db.add(user_model)
    db.commit()