from fastapi import APIRouter, Response

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.users import AddRequestUser
from app.services.auth import AuthService


auth_router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@auth_router.get("/me")
async def get_user_info(db: DBDep, user_id: UserIdDep):
    user_data = await AuthService(db).get_me(user_id)
    return {"message": "Информация о текущем пользователе", "detail": user_data}


@auth_router.post("/register")
async def register_user(db: DBDep, data: AddRequestUser):
    await AuthService(db).register(data)
    return {"message": "Пользователь успешно зарегистрирован"}


@auth_router.post("/login")
async def login_user(db: DBDep, data: AddRequestUser, response: Response):
    access_token = await AuthService(db).login(data, response)
    return {"access_token": access_token}


@auth_router.get("/logout")
async def logout_user(db: DBDep, response: Response):
    await AuthService(db).logout(response)
    return {"message": "Вы успешно вышли из системы"}