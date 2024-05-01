import uvicorn
from fastapi import FastAPI

from app.routes.authorization import router as auth_router
from app.routes.test_data import router as test_router, create_test_data
from app.routes.main_page import router as main_page_router
from app.routes.crud_desk import router as desk_router
from app.routes.crud_user import router as user_router
from app.routes.crud_task import router as task_router
from app.db.core import create_tables


app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(desk_router, prefix="/desk")
app.include_router(task_router, prefix="/task")
app.include_router(main_page_router)
app.include_router(test_router)
app.include_router(auth_router)

if __name__ == '__main__':
    create_tables()
    create_test_data()

    uvicorn.run(app,
                host='127.0.0.1',
                port=8080)
