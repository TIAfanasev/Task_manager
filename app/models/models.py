from pydantic import BaseModel, field_validator
from typing import Union
import re

class LogPass(BaseModel):
    login: str
    password: str