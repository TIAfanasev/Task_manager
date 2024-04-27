from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import insert_user, pass_for_login, get_user_from_db, add_tokens
from app.utils import create_access_token, create_refresh_token, check_refresh_token_valid

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


# Проверка корректности логина и пароля
def check_user_correct(login, password):
    current_pass = pass_for_login(login)
    if current_pass:
        if password == current_pass:
            return True
    return False


@router.post("/login")
async def authenticate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if check_user_correct(form_data.username, form_data.password):
        user_id, role = get_user_from_db(form_data.username)
        access_token = await create_access_token(user_id, role)
        refresh_token = await create_refresh_token(user_id, role)
        add_tokens(user_id, access_token, refresh_token)
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"}
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/login/refresh_token")
async def generate_new_tokens(token: dict = Depends(check_refresh_token_valid)):
    return token


