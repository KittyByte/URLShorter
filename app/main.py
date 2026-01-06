import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import uvicorn
from fastapi import FastAPI

from app.users.routers import router as users_router
from app.api_services.routers import router as api_services_router


app = FastAPI()
app.include_router(users_router)
app.include_router(api_services_router)



if __name__ == "__main__":
    uvicorn.run('app.main:app', reload=True, host='0.0.0.0', port=8000)

