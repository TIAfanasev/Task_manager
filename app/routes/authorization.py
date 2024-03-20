from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import insert_user, pass_for_login

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def gen_token(payload):
    # обдумать и доделать!!!!!!!
    return jwt.encode({"sub": payload}, SECRET_KEY, algorithm=ALGORITHM)


# Проверка корректности логина и пароля
def check_user_correct(login, password):
    current_pass = pass_for_login(login)
    print(current_pass)
    if current_pass:
        if password == current_pass[0]:
            return True
    return False


@router.post("/login")
async def authenticate_user(input_data: md.LogPass):
    if check_user_correct(input_data.login, input_data.password):
        return gen_token(input_data.login)
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/create_user")
async def create_user(input_data: md.User):
    if not input_data.new_user_invalid():
        insert_user(input_data.login, input_data.password, input_data.name, input_data.role)
        return {"status": "success"}
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")
