from routes import authorization
import uvicorn
from fastapi import FastAPI

app = FastAPI()

app.include_router(authorization.router)

if __name__ == '__main__':
    uvicorn.run(app,
                host='127.0.0.1',
                port=8080)