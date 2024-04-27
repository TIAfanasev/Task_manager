import datetime

from pydantic import BaseModel, field_validator
from typing import Union, List, Tuple
import re


class LogPass(BaseModel):
    username: str
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
    id: int | None
    desk_name: str
    invite_code: str | None
    admin_id: int
    description: str

    def new_desk_invalid(self):
        print(self.desk_name)
        return False


class Task(BaseModel):
    id: int | None
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


class MainTasksOutput(BaseModel):
    id: int
    desk_id: int
    task_name: str
    description: str
    deadline: datetime.date


class UserInfo(BaseModel):
    id: int
    login: str
    name: str
    role: int


class TasksInfoForOneDesk(BaseModel):
    id: int
    desk_id: int
    task_name: str
    description: str
    creator_id: int
    status_id: int
    creation_date: datetime.date
    deadline: datetime.date
    users_list: List[UserInfo]


class InputUsersAddToTask(BaseModel):
    task_id: int
    user_list: list[int]
