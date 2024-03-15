from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
import uvicorn
import models.models as md
import random
import jwt
from users import User
from fastapi import APIRouter

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

def gen_token(payload):
     #обдумать и доделать!!!!!!!
     return jwt.encode({"sub":payload}, SECRET_KEY, algorithm=ALGORITHM)

def check_user_correct(login, password):
     print('Zaglushka')
     return True

@router.post("/login")
async def authenticate_user(input_data:md.LogPass):
     if check_user_correct(input_data.login, input_data.password):
          return(gen_token(input_data.login))
     else:
          return HTTPException(status_code=401, detail="Invalid credentials")