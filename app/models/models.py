from pydantic import BaseModel, field_validator
from typing import Union
import re


class LogPass(BaseModel):
    login: str
    password: str


class User(BaseModel):
    login: str
    password: str
    name: str
    role: str

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
