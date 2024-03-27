from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy import Integer, and_, func, insert, select, text, update
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import insert_user, pass_for_login
from app.db.database import sync_engine
from app.db.models import metadata, users_table, desks_table, tasks_table, status_table, users_tasks_table

router = APIRouter()


@router.post("/test_data")
async def create_test_data():
    with sync_engine.connect() as conn:
        stmt = insert(users_table).values(
            [
                {"login": 'user1',
                 "hash_pass": 'fn2oin02jc933d2sok',
                 "name": 'Boris',
                 "role": 1}
            ]
        )
        conn.execute(stmt)
        conn.commit()

    with sync_engine.connect() as conn:
        stmt = insert(desks_table).values(
            [
                {"desk_name": "desk1",
                 "invite_code": "fn2vjenov4nfd2hd0",
                 "admin_id": 1,
                 "description": "test desk"},
                {"desk_name": "desk2",
                 "invite_code": "gjsvnur83ndis",
                 "admin_id": 1,
                 "description": "test desk"}
            ]
        )
        conn.execute(stmt)
        conn.commit()

    with sync_engine.connect() as conn:
        stmt = insert(tasks_table).values(
            [
                {"desk_id": 1,
                 "task_name": "task1",
                 "description": "descr_of_the_task",
                 "creator_id": 1,
                 "status_id": 1,
                 "creation_date": "2001-08-22",
                 "deadline": "2024-08-22"},
                {"desk_id": 2,
                 "task_name": "task2",
                 "description": "descr_of_the_task",
                 "creator_id": 1,
                 "status_id": 1,
                 "creation_date": "2001-08-22",
                 "deadline": "2024-08-22"}
            ]
        )
        conn.execute(stmt)
        conn.commit()

    with sync_engine.connect() as conn:
        stmt = insert(users_tasks_table).values(
            [
                {"user_id": 1,
                 "task_id": 1},
                {"user_id": 1,
                 "task_id": 2},
            ]
        )
        conn.execute(stmt)
        conn.commit()
