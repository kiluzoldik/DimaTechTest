from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import AccountNotFoundException, AccountNotFoundHTTPException, DeleteAccountBalanceNotNullException, DeleteAccountBalanceNotNullHTTPException
from app.services.accounts import AccountService


account_router = APIRouter(
    prefix="/accounts", 
    tags=["Финансовый счёт активного пользователя"]
)


@account_router.get("/me", summary="Финансовые счета", description="<h1>Финансовые счета активного пользователя</h1>")
async def get_my_accounts(db: DBDep, user_id: UserIdDep):
    accounts = await AccountService(db).get_accounts(user_id)
    return accounts


@account_router.get("/{account_id}", summary="Финансовый счет", description="<h1>Выбранный финансовый счет активного пользователя</h1>")
async def get_account(db: DBDep, user_id: UserIdDep, account_id: int):
    try:
        account = await AccountService(db).get_account_by_user(account_id, user_id)
    except AccountNotFoundException:
        raise AccountNotFoundHTTPException
    
    return account


@account_router.post("", summary="Создание финансового счета", description="<h1>Создание финансового счета для активного пользователя</h1>")
async def create_account(db: DBDep, user_id: UserIdDep):
    await AccountService(db).create_account(user_id)
    return {"message": "Счёт успешно создан"}


@account_router.delete("/{account_id}", summary="Удаление финансового счета", description="<h1>Удаление финансового счета активного пользователя</h1>")
async def delete_account(db: DBDep, user_id: UserIdDep, account_id: int):
    try:
        await AccountService(db).delete_account(account_id, user_id)
    except AccountNotFoundException:
        raise AccountNotFoundHTTPException
    except DeleteAccountBalanceNotNullException:
        raise DeleteAccountBalanceNotNullHTTPException
    
    return {"message": "Счёт успешно удален"}