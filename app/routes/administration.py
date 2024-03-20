from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import create_new_desk

router = APIRouter()


@router.post("/create_desk")
async def create_desk(input_data: md.Desk):
    if not input_data.new_desk_invalid():
        create_new_desk(input_data.desk_name, input_data.invite_code, input_data.admin_id, input_data.description)
        return {"status": "success"}
    else:
        return HTTPException(status_code=401, detail="Invalid credentials")
