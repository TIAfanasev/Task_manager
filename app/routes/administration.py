from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import create_new_desk, create_new_task, users_in_task, insert_user, get_desks_for_user
from app.utils import check_access_token_valid

router = APIRouter()


@router.put("/task")
async def add_users_to_task(input_data: md.InputUsersAddToTask,
                            token: dict = Depends(check_access_token_valid)
                            ):
    if token.get("role") in (2, 3):
        if input_data.user_list:
            users_in_task(input_data.task_id, input_data.user_list)
            return {"status": "success"}
        else:
            return HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return HTTPException(status_code=403, detail="Forbidden")


