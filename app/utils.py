from datetime import datetime, timedelta
from typing import Union, Any
import jwt
from fastapi import FastAPI, Cookie, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm


from app.config import settings
from app.db.core import get_user_tokens, add_tokens

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = settings.JWT_SECRET_KEY  # should be kept secret
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY  # should be kept secret

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def create_access_token(user_id, role, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode({"exp": expires_delta, "user_id": user_id, "role": role}, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def create_refresh_token(user_id, role, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode({"exp": expires_delta, "user_id": user_id, "role": role}, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def check_access_token_valid(token: str = Depends(oauth2_scheme)):
    if token:
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            if token == get_user_tokens(True, user_id):
                return payload
            else:
                raise HTTPException(status_code=401, detail="Fake access token!")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Access token out of time")
        except jwt.InvalidTokenError:
            pass  # тут какая-то логика обработки ошибки декодирования токена
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def check_refresh_token_valid(token: str = Depends(oauth2_scheme)):
    if token:
        try:
            payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            role = payload.get("role")
            if token == get_user_tokens(False, user_id):
                access_token = await create_access_token(user_id, role)
                refresh_token = await create_refresh_token(user_id, role)
                add_tokens(user_id, access_token, refresh_token)
                return {"access_token": access_token,
                        "refresh_token": refresh_token,
                        "token_type": "bearer"}
            else:
                raise HTTPException(status_code=401, detail="Fake refresh token!")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token out of time")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid RT")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
