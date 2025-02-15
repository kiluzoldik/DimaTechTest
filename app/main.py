import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from app.api.auth import auth_router
from app.api.accounts import account_router
from app.api.payments import payment_router
from app.api.admins import admin_router


app = FastAPI()

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(account_router)
app.include_router(payment_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True)