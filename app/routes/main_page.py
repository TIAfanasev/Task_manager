from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import (create_new_desk, create_new_task, users_in_task, get_user_from_db, get_desks_for_user,
                         get_most_important_tasks)
from app.utils import create_refresh_token, create_access_token, check_refresh_token_valid, check_access_token_valid


router = APIRouter()


@router.get("/main_desks")
async def get_desk(
        token: dict = Depends(check_access_token_valid)
) -> list[md.Desk]:
    print(token)
    desks = get_desks_for_user(token.get("user_id"))
    return desks


@router.get("/main_tasks")
async def get_important_tasks(
    token: dict = Depends(check_access_token_valid)
) -> list[md.MainTasksOutput]:
    tasks = get_most_important_tasks(token.get("user_id"))
    return tasks

