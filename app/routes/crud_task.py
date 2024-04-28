from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
import app.models.models as md
import random
import jwt
from app.db.core import create_new_desk, create_new_task, users_in_task, insert_user, get_desks_for_user
from app.utils import check_access_token_valid

router = APIRouter()


# создание новой задачи на доске
@router.post("/task")
async def create_task(input_data: md.Task,
                      token: dict = Depends(check_access_token_valid)
                      ):
    if token.get("role") in (2, 3):
        if not input_data.new_task_invalid():
            create_new_task(input_data.desk_id,
                            input_data.task_name,
                            input_data.description,
                            input_data.creator_id,
                            input_data.status_id,
                            input_data.creation_date,
                            input_data.deadline)
            return {"status": "success"}
        else:
            return HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return HTTPException(status_code=403, detail="Forbidden")


@router.get("/task/{task_id}")
async def task_information(
        task_id: int,
        token: dict = Depends(check_access_token_valid)
):
    current_user_id = token.get("user_id")
    role = token.get("role")
    # user_info = get_user_info(user_id)
    # if role == 3 or current_user_id == user_id:
    #     return user_info
    # else:
    #     return HTTPException(status_code=403, detail="Forbidden")