import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import uvicorn
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.users.routers import router as users_router
from app.api_services.routers import router as api_services_router
from app.url_short.routers import router as url_short_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield


app = FastAPI(default_response_class=ORJSONResponse)

app.include_router(users_router)
app.include_router(api_services_router)
app.include_router(url_short_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if __name__ == "__main__":
    uvicorn.run('app.main:app', reload=True, host='0.0.0.0', port=8000)

