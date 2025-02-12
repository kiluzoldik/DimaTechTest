from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import SignatureValidationException, SignatureValidationHTTPException, TransactionIdAlreadyExistsException, TransactionIdAlreadyExistsHTTPException
from app.schemas.payments import AddRequestPayment
from app.services.payments import PaymentService


payment_router = APIRouter(tags=["Создание платежа для счета"])


@payment_router.get("/payments/me", summary="Получение транзакций", description="<h1>Получение всех платежных транзакций активного пользователя</h1>")
async def get_my_payments(db: DBDep, user_id: UserIdDep):
    return await PaymentService(db).get_transactions_history(user_id)


@payment_router.post("/{account_id}/payments", summary="Создание платежа/транзакции")
async def make_payment(db: DBDep, user_id: UserIdDep, data: AddRequestPayment):
    try:
        await PaymentService(db).create_transaction(data, user_id)
    except SignatureValidationException:
        raise SignatureValidationHTTPException
    except TransactionIdAlreadyExistsException:
        raise TransactionIdAlreadyExistsHTTPException
    
    return {"message": "Платеж успешно завершен"}
