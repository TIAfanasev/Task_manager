from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import insert_user

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def gen_token(payload):
    # обдумать и доделать!!!!!!!
    return jwt.encode({"sub": payload}, SECRET_KEY, algorithm=ALGORITHM)


def check_user_correct(login, password):
    print('Zaglushka')
    return True

def new_user_invalid(log, pas, name, role):
    print('Zaglushka')
    return False


@router.post("/login")
async def authenticate_user(input_data: md.LogPass):
    if check_user_correct(input_data.login, input_data.password):
        return gen_token(input_data.login)
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/create_user")
async def create_user(input_data: md.User):
    if not new_user_invalid(input_data.login, input_data.password, input_data.name, input_data.role):
        insert_user(input_data.login, input_data.password, input_data.name, input_data.role)
        return {"status": "success"}
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")


