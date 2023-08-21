from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime
import starlette.status as status


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)
bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl= 'auth/token')

#* JWT 만들기 위해서는 SECRET_KEY 와 ALGORITHM 이 필요하다
#* openssl rand -hex 32 : 랜덤한 32글자 String 만들기 
SECRET_KEY = 'a3b0db5dd6310841af59b8a7bbf1e4aa9d15b147d7cd07f773b0e6c016aa2325'
ALGORITHM = 'HS256'

class CreateUserRequest(BaseModel):
    email : str
    username : str
    first_name : str 
    last_name : str
    password : str
    role : str

class Token(BaseModel):
    access_token : str
    token_type : str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Depends : get_db 함수에 의존한다 -> db 열고 닫기 
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id : int, role: str, expires_data : timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expire = datetime.utcnow() + expires_data
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(statue_code = status.HTTP_401_UNAUTHORIZED,
                                detail = 'Could not validate user')
        return {'username':username, 'id':user_id, 'role': user_role}
    except JWTError:
        HTTPException(statue_code = status.HTTP_401_UNAUTHORIZED,
                                detail = 'Could not validate user')



#* models의 Users 와 이름이 다르므로 일일히 타이핑 해줬다(hashed_password, password)
#* bcrypt_context.hash : password 를 hashing 하는 알고리즘 
@router.post("/")
async def create_user(db: db_dependency,
                    create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )
    db.add(create_user_model)
    db.commit()
    

@router.post("/token", response_model = Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
                                db : db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(statue_code = status.HTTP_401_UNAUTHORIZED,
                                detail = 'Could not validate user')
    token = create_access_token(user.username, user.id, user.role ,timedelta(minutes=20))
    
    return {'access_token':token, 'token_type': 'bearer'}