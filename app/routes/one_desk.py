from fastapi import FastAPI, Cookie, HTTPException, Request, Header, Depends, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.encoders import jsonable_encoder
from typing import Annotated, List, Any, Union
import uvicorn
import app.models.models as md
import random
import jwt
from app.db.core import get_all_tasks_for_desk, get_desk_info, get_user_info, update_desk_info
from app.utils import check_refresh_token_valid, check_access_token_valid


router = APIRouter()

