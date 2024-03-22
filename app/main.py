import uvicorn
from fastapi import FastAPI

from app.routes.authorization import router as auth_router
from app.routes.administration import router as admin_router
from app.db.core import create_tables

import datetime


app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router, prefix="/create")

if __name__ == '__main__':
    create_tables()
    print(datetime.date(2000, 8, 22))
    uvicorn.run(app,
                host='127.0.0.1',
                port=8080)
