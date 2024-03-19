import os
import sys

import uvicorn
from fastapi import FastAPI

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from routes.authorization import router
from db.core import create_tables


app = FastAPI()

app.include_router(router)

if __name__ == '__main__':
    create_tables()

    uvicorn.run(app,
                host='127.0.0.1',
                port=8080)
