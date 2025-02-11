from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.services.accounts import AccountService


account_router = APIRouter(
    prefix="/accounts", 
    tags=["Финансовый счёт активного пользователя"]
)


@account_router.get("/me")
async def get_my_accounts(db: DBDep, user_id: UserIdDep):
    accounts = await AccountService(db).get_accounts(user_id)
    return accounts


@account_router.get("/{account_id}")
async def get_account(db: DBDep, user_id: UserIdDep, account_id: int):
    account = await AccountService(db).get_account_by_user(account_id, user_id)
    return account


@account_router.post("")
async def create_account(db: DBDep, user_id: UserIdDep):
    await AccountService(db).create_account(user_id)
    return {"message": "Счёт успешно создан"}


@account_router.delete("/{account_id}")
async def delete_account(db: DBDep, user_id: UserIdDep, account_id: int):
    await AccountService(db).delete_account(account_id, user_id)
    return {"message": "Счёт успешно удален"}