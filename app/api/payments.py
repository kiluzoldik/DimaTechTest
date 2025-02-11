from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.payments import AddRequestPayment
from app.services.payments import PaymentService


payment_router = APIRouter(tags=["Создания платежа для счета"])


@payment_router.get("/payments/me")
async def get_my_payments(db: DBDep, user_id: UserIdDep):
    payments = await PaymentService(db).get_transactions_history(user_id)
    return payments


@payment_router.post("/{account_id}/payments")
async def make_payment(db: DBDep, user_id: UserIdDep, data: AddRequestPayment):
    await PaymentService(db).create_transaction(data, user_id)
    return {"message": "Платеж успешно завершен"}
