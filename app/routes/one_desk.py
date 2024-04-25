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
from app.utils import check_refresh_token_valid, check_access_token_valid


router = APIRouter()


@router.get("/desk/{desk_id}", response_model=List[md.TasksInfoForOneDesk])
async def get_desk(
        desk_id: int,
        token: int = Depends(check_access_token_valid)
):
    desk_info = get_all_tasks_for_desk(desk_id)
    print(desk_info)
    return desk_info
