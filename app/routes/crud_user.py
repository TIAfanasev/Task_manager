from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
import app.models.models as md
import random
import jwt
from app.db.core import create_new_desk, create_new_task, users_in_task, insert_user, get_desks_for_user, get_user_info, \
    delete_one_user
from app.utils import check_access_token_valid

router = APIRouter()


# создание нового пользователя (admin role only)
@router.post("/user")
async def create_user(input_data: md.UserCreateModel,
                      token: dict = Depends(check_access_token_valid)
                      ):
    if token.get("role") == 3:
        if not input_data.new_user_invalid():
            insert_user(input_data.login, input_data.password, input_data.name, input_data.role)
            return {"status": "success"}
        else:
            return HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return HTTPException(status_code=403, detail="Forbidden")


# получение информации о пользователе
@router.get("/user/{user_id}", response_model=md.UserInfo)
async def user_information(
        user_id: int,
        token: dict = Depends(check_access_token_valid)
):
    current_user_id = token.get("user_id")
    role = token.get("role")
    user_info = get_user_info(user_id)
    if role == 3 or current_user_id == user_id:
        return user_info
    else:
        return HTTPException(status_code=403, detail="Forbidden")


# обновление информации о пользователе
@router.put("/user/{user_id}")
async def user_update(
        user_id: int,
        input_data: md.UserInfoUpdate,
        token: dict = Depends(check_access_token_valid)
):
    #НАПИСАТЬ ПО АНАЛОГИИ С ДЕСКОЙ
    pass


# удаление пользователя
@router.delete("/user/{user_id}")
async def user_delete(
        user_id: int,
        token: dict = Depends(check_access_token_valid)
):
    role = token.get("role")
    if role == 3:
        delete_one_user(user_id)
        return {"details": "success"}
    else:
        return HTTPException(status_code=403, detail="Forbidden")
