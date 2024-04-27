from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from typing import Annotated, List, Any, Union
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import get_all_tasks_for_desk, get_desk_info, get_user_info, update_desk_info
from app.utils import check_refresh_token_valid, check_access_token_valid


router = APIRouter()


@router.get("/desk/{desk_id}", response_model=List[md.TasksInfoForOneDesk])
async def get_desk(
        desk_id: int,
        token: dict = Depends(check_access_token_valid)
):
    desk_info = get_all_tasks_for_desk(desk_id)
    print(desk_info)
    return desk_info


@router.post("/desk/{desk_id}", response_model=md.Desk)
async def update_desk(
        input_data: md.Desk,
        token: dict = Depends(check_access_token_valid)
):
    user_id = token.get("user_id")
    role = token.get("role")
    current_desk = get_desk_info(input_data.id)
    current_desk = current_desk._asdict()
    if role == 3 or current_desk.admin_id == user_id:
        if current_desk['desk_name'] != input_data.desk_name and input_data.desk_name:
            current_desk['desk_name'] = input_data.desk_name
        if current_desk['description'] != input_data.description and input_data.description:
            current_desk['description'] = input_data.description
        if input_data.admin_id:
            new_admin = get_user_info(input_data.admin_id)
            if new_admin.role in (2, 3):
                current_desk['admin_id'] = input_data.admin_id
            else:
                raise HTTPException(status_code=400, detail="New admin have user role")
        return get_desk_info(update_desk_info(current_desk))
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
