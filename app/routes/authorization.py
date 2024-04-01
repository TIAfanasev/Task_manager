from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import insert_user, pass_for_login, get_user_from_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def gen_token(payload):
    # обдумать и доделать!!!!!!!
    return jwt.encode({"sub": payload}, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # декодируем токен
        return payload.get("sub")  # тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере (
        # subject); обычно там еще можно взять "iss" - issuer/эмитент, или "exp" - expiration time - время 'сгорания'
        # и другое, что мы сами туда кладем
    except jwt.ExpiredSignatureError:
        pass  # тут какая-то логика ошибки истечения срока действия токена
    except jwt.InvalidTokenError:
        pass  # тут какая-то логика обработки ошибки декодирования токена


# Проверка корректности логина и пароля
def check_user_correct(login, password):
    current_pass = pass_for_login(login)
    if current_pass:
        if password == current_pass:
            return True
    return False


@router.post("/login")
async def authenticate_user(input_data: md.LogPass):
    if check_user_correct(input_data.login, input_data.password):
        user_id, role = get_user_from_db(input_data.login)
        subject = {"user_id": user_id, "role": role}
        return {"access_token": gen_token(subject), "token_type": "bearer"}
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/create_user")
async def create_user(input_data: md.UserCreateModel):
    if not input_data.new_user_invalid():
        insert_user(input_data.login, input_data.password, input_data.name, input_data.role)
        return {"status": "success"}
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")
