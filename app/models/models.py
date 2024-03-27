import datetime

from pydantic import BaseModel, field_validator
from typing import Union
import re


class LogPass(BaseModel):
    login: str
    password: str


class UserCreateModel(BaseModel):
    login: str
    password: str
    name: str
    role: int

    def new_user_invalid(self):
        print(self.login)
        return False


class Desk(BaseModel):
    desk_name: str
    invite_code: str
    admin_id: int
    description: str

    def new_desk_invalid(self):
        print(self.desk_name)
        return False


class Task(BaseModel):
    desk_id: int
    task_name: str
    description: str
    creator_id: int
    status_id: int
    creation_date: datetime.date
    deadline: datetime.date

    def new_task_invalid(self):
        print(self.task_name)
        return False