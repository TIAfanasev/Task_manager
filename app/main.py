import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.routes.authorization import router as auth_router
from app.routes.administration import router as admin_router
from app.routes.test_data import router as test_router
from app.routes.main_page import router as main_page_router
from app.routes.one_desk import router as one_desk_router
from app.db.core import create_tables

import datetime


app = FastAPI()

app.include_router(main_page_router)
app.include_router(test_router)
app.include_router(auth_router)
app.include_router(one_desk_router)
app.include_router(admin_router, prefix="/create")

if __name__ == '__main__':
    create_tables()
    print(datetime.date(2000, 8, 22))
    uvicorn.run(app,
                host='127.0.0.1',
                port=8080)
