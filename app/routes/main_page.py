from fastapi import Depends, APIRouter
import app.models.models as md
from app.db.core import get_desks_for_user, get_most_important_tasks
from app.utils import check_access_token_valid


router = APIRouter()


@router.get("/main_desks")
async def get_desk(
        token: dict = Depends(check_access_token_valid)
) -> list[md.Desk]:
    print(token)
    desks = get_desks_for_user(token.get("user_id"))
    return desks


@router.get("/main_tasks")
async def get_important_tasks(
    token: dict = Depends(check_access_token_valid)
) -> list[md.MainTasksOutput]:
    tasks = get_most_important_tasks(token.get("user_id"))
    return tasks

