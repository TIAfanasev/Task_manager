from typing import List

from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
import app.models.models as md
import random
import jwt
from app.db.core import create_new_desk, create_new_task, users_in_task, insert_user, get_desks_for_user, \
    get_all_tasks_for_desk, get_desk_info, get_user_info, update_desk_info, delete_one_desk
from app.models.models import Desk
from app.utils import check_access_token_valid

router = APIRouter()


# создание новой доски
@router.post("/create")
async def create_desk(input_data: md.Desk,
                      token: dict = Depends(check_access_token_valid)
                      ):
    if token.get("role") in (2, 3):
        if not input_data.new_desk_invalid():
            create_new_desk(input_data.desk_name,
                            input_data.invite_code,
                            input_data.admin_id,
                            input_data.description)
            return {"status": "success"}
        else:
            return HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return HTTPException(status_code=403, detail="Forbidden")


# получение информации о доске
@router.get("/{desk_id}", response_model=md.FullDeskInfo)
async def desk_information(
        desk_id: int,
        token: dict = Depends(check_access_token_valid)
):
    desk_info = get_desk_info(desk_id)
    return desk_info


# Обновление информации о доске
@router.put("/{desk_id}", response_model=md.Desk)
async def desk_update(
        input_data: md.Desk,
        token: dict = Depends(check_access_token_valid)
):
    user_id = token.get("user_id")
    role = token.get("role")
    current_desk = get_desk_info(input_data.id)
    current_desk = current_desk._asdict()
    if role == 3 or current_desk['admin_id'] == user_id:
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


# удаление информации о доске
@router.delete("/{desk_id}")
async def desk_delete(
        desk_id: int,
        token: dict = Depends(check_access_token_valid)
):
    user_id = token.get("user_id")
    role = token.get("role")
    desk_info = get_desk_info(desk_id)
    if role == 3 or desk_info.admin_id == user_id:
        delete_one_desk(desk_id)
        return {"details": "success"}
    else:
        return HTTPException(status_code=403, detail="Forbidden")
