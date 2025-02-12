from fastapi import APIRouter

from app.api.dependencies import AdminDep, DBDep
from app.exceptions import UserEmailAlreadyExistsException, UserEmailAlreadyExistsHTTPException, UserNotFoundException, UserNotFoundHTTPException
from app.schemas.users import AddRequestUser, FullEditUser, PartialEditUser
from app.services.admins import AdminService
from app.services.auth import AuthService


admin_router = APIRouter(prefix="/admin", tags=["Ручки для администратора"])


@admin_router.get("/users", summary="Все пользователи", description="<h1>Получение всех пользователей</h1>", dependencies=[AdminDep])
async def get_users(db: DBDep):
    return await AdminService(db).get_all_users()


@admin_router.get("/users/{user_id}/accounts", summary="Счета пользователя", description="<h1>Получение всех финансовых счетов пользователя</h1>", dependencies=[AdminDep])
async def get_accounts_by_user(db: DBDep, user_id: int):
    try:
        return await AdminService(db).get_accounts_with_payments_by_user(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@admin_router.post("/users", summary="Создание пользователя", description="<h1>Создание нового пользователя</h1>", dependencies=[AdminDep])
async def register_user(db: DBDep, data: AddRequestUser):
    try:
        await AuthService(db).register(data)
    except UserEmailAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    
    return {"message": "Пользователь успешно зарегистрирован"}


@admin_router.put("/users/{user_id}", summary="Полное обновление", description="<h1>Полное обновление данных пользователя</h1>", dependencies=[AdminDep])
async def full_update_user(db: DBDep, user_id: int, data: FullEditUser):
    try:
        await AdminService(db).full_update_user(user_id, data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
        
    return {"message": "Пользователь успешно изменён"}


@admin_router.patch("/users/{user_id}", summary="Частичное обновление", description="<h1>Частичное обновление данных пользователя</h1>", dependencies=[AdminDep])
async def partial_update_user(db: DBDep, user_id: int, data: PartialEditUser):
    try:
        await AdminService(db).partial_update_user(user_id, data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
        
    return {"message": "Пользователь успешно изменён"}


@admin_router.delete("/users/{user_id}", summary="Удаление пользователя", description="<h1>Удаление выбранного пользователя</h1>", dependencies=[AdminDep])
async def delete_user(db: DBDep, user_id: int):
    try:
        await AdminService(db).delete_user(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
        
    return {"message": "Пользователь успешно удалён"}
