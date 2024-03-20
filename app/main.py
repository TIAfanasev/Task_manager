import uvicorn
from fastapi import FastAPI

from app.routes.authorization import router as auth_router
from app.routes.administration import router as admin_router
from app.db.core import create_tables


app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)

if __name__ == '__main__':
    create_tables()

    uvicorn.run(app,
                host='127.0.0.1',
                port=8080)
