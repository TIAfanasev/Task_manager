from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import insert_user, pass_for_login, get_user_from_db
from app.utils import create_access_token, create_refresh_token

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def gen_token(payload):
    # обдумать и доделать!!!!!!!
    return jwt.encode({"sub": payload}, SECRET_KEY, algorithm=ALGORITHM)


# def get_user_from_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # декодируем токен
#         return payload.get("sub")  # тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере (
#         # subject); обычно там еще можно взять "iss" - issuer/эмитент, или "exp" - expiration time - время 'сгорания'
#         # и другое, что мы сами туда кладем
#     except jwt.ExpiredSignatureError:
#         pass  # тут какая-то логика ошибки истечения срока действия токена
#     except jwt.InvalidTokenError:
#         pass  # тут какая-то логика обработки ошибки декодирования токена


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
        return {"access_token": await create_access_token(user_id, role),
                "refresh_token": await create_refresh_token(user_id, role),
                "token_type": "bearer"}
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")

