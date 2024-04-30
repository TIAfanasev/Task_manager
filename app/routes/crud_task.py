from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
import app.models.models as md
import random
import jwt
from app.db.core import create_new_desk, create_new_task, users_in_task, insert_user, get_desks_for_user, get_task_info, \
    update_task_info, delete_one_task
from app.utils import check_access_token_valid

router = APIRouter()


# создание новой задачи на доске
@router.post("/create")
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


@router.get("/{task_id}")
async def task_information(
        task_id: int,
        token: dict = Depends(check_access_token_valid)
):
    current_user_id = token.get("user_id")
    role = token.get("role")
    task_info = get_task_info(task_id)
    if role == 3 or task_info.creator_id == current_user_id:
        return task_info
    else:
        return HTTPException(status_code=403, detail="Forbidden")


@router.put("/{task_id}")
async def task_update(
        task_id: int,
        input_data: md.TasksInfoForOneDesk,
        token: dict = Depends(check_access_token_valid)
):
    current_user_id = token.get("user_id")
    role = token.get("role")
    current_task = get_task_info(task_id=task_id)
    current_task = current_task._asdict()
    if role == 3 or current_task["creator_id"] == current_user_id:
        if input_data.task_name != current_task["task_name"]:
            current_task["task_name"] = input_data.task_name
        if input_data.description != current_task["description"]:
            current_task["description"] = input_data.description
        if input_data.status_id != current_task["status_id"]:
            current_task["status_id"] = input_data.status_id
        if input_data.deadline != current_task["deadline"]:
            current_task["deadline"] = input_data.deadline
        if input_data.users_list.sort() != current_task["users_list"].sort():
            current_task["users_list"] = input_data.users_list
        return get_task_info(update_task_info(current_task))


@router.delete("/{task_id}")
async def task_delete(
        task_id: int,
        token: dict = Depends(check_access_token_valid)
):
    current_user_id = token.get("user_id")
    role = token.get("role")
    current_task = get_task_info(task_id=task_id)
    if role == 3 or current_task.creator_id == current_user_id:
        delete_one_task(task_id)
        return {"details": "success"}
    else:
        return HTTPException(status_code=403, detail="Forbidden")
