import datetime

from pydantic import BaseModel
from typing import List, Optional


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
    id: Optional[int] = None
    desk_name: str
    invite_code: Optional[str] = None
    admin_id: int
    description: str

    def new_desk_invalid(self):
        print(self.desk_name)
        return False


class UserInfo(BaseModel):
    id: int
    login: str
    name: str
    role: int


class Task(BaseModel):
    # id: Optional[int] = None
    desk_id: int
    task_name: str
    description: str
    creator_id: int
    status_id: int
    creation_date: datetime.date
    deadline: datetime.date
    users_list: Optional[List[UserInfo]] = None

    def new_task_invalid(self):
        print(self.task_name)
        return False


class MainTasksOutput(BaseModel):
    id: int
    desk_id: int
    task_name: str
    description: str
    deadline: datetime.date


class TasksInfoForOneDesk(BaseModel):
    id: Optional[int] = None
    desk_id: Optional[int] = None
    task_name: Optional[str] = None
    description: Optional[str] = None
    creator_id: Optional[int] = None
    status_id: Optional[int] = None
    creation_date: Optional[datetime.date] = None
    deadline: Optional[datetime.date] = None
    users_list: Optional[List[UserInfo]] = None


class InputUsersAddToTask(BaseModel):
    task_id: int
    user_list: list[int]


class UserInfoUpdate(BaseModel):
    password: str
    name: str
    role: int


class FullDeskInfo(BaseModel):
    id: Optional[int] = None
    desk_name: Optional[str] = None
    invite_code: Optional[str] = None
    admin_id: Optional[int] = None
    description: Optional[str] = None
    tasks_list: Optional[List[TasksInfoForOneDesk]] = None
