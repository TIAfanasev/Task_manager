from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from typing import Annotated, List, Any
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import get_all_tasks_for_desk
from app.routes.authorization import get_user_from_token


router = APIRouter()


@router.get("/desk/{desk_id}", response_model=List[md.TasksInfoForOneDesk])
async def get_desk(
        desk_id: int,
        token: int = Depends(get_user_from_token)
):
    print(token)
    desk_info = get_all_tasks_for_desk(desk_id)
    print(desk_info)
    return desk_info
