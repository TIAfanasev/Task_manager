from fastapi import HTTPException, Depends, APIRouter
import app.models.models as md
from app.db.core import insert_user, get_user_info, delete_one_user, update_user_info
from app.utils import check_access_token_valid

router = APIRouter()


# создание нового пользователя (admin role only)
@router.post("/create")
async def create_user(input_data: md.UserCreateModel,
                      token: dict = Depends(check_access_token_valid)
                      ):
    if token.get("role") == 3:
        if not input_data.new_user_invalid():
            insert_user(input_data.login, input_data.password, input_data.name, input_data.role)
            return {"status": "success"}
        else:
            return HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return HTTPException(status_code=403, detail="Forbidden")


# получение информации о пользователе
@router.get("/{user_id}", response_model=md.UserInfo)
async def user_information(
        user_id: int,
        token: dict = Depends(check_access_token_valid)
):
    current_user_id = token.get("user_id")
    role = token.get("role")
    user_info = get_user_info(user_id)
    if role == 3 or current_user_id == user_id:
        return user_info
    else:
        return HTTPException(status_code=403, detail="Forbidden")


# обновление информации о пользователе
@router.put("/{user_id}", response_model=md.UserInfo)
async def user_update(
        user_id: int,
        input_data: md.UserInfoUpdate,
        token: dict = Depends(check_access_token_valid)
):
    current_user_id = token.get("user_id")
    role = token.get("role")
    current_user = get_user_info(user_id)
    current_user = current_user._asdict()
    if user_id == current_user_id or role == 3:
        if input_data.password != current_user["hash_pass"]:
            current_user["hash_pass"] = input_data.password
        if input_data.name != current_user["name"]:
            current_user["name"] = input_data.name
        if input_data.role != current_user["role"]:
            if input_data.role not in (1, 3):
                raise HTTPException(status_code=400, detail="Wrong role")
            if role == 3:
                current_user["role"] = input_data.role
            else:
                if input_data.role < current_user["role"]:
                    current_user["role"] = input_data.role
                else:
                    raise HTTPException(status_code=403, detail="Forbidden")
        update_user_info(current_user)
        user_info = get_user_info(user_id)
        return user_info
    return HTTPException(status_code=403, detail="Forbidden")


# удаление пользователя
@router.delete("/{user_id}")
async def user_delete(
        user_id: int,
        token: dict = Depends(check_access_token_valid)
):
    role = token.get("role")
    if role == 3:
        delete_one_user(user_id)
        return {"details": "success"}
    else:
        return HTTPException(status_code=403, detail="Forbidden")
