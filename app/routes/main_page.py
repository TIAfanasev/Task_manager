from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import create_new_desk, create_new_task, users_in_task, get_user_from_db, get_desks_for_user, get_most_important_tasks
from app.routes.authorization import get_user_from_token


router = APIRouter()


@router.get("/main_desks")
async def get_desk(
        token: int = Depends(get_user_from_token)
) -> list[md.Desk]:
    print(token)
    desks = get_desks_for_user(token)
    return desks


@router.get("/main_tasks")
async def get_important_tasks(
    token: int = Depends(get_user_from_token)
) -> list[md.MainTasksOutput]:
    tasks = get_most_important_tasks(token)
    return tasks

