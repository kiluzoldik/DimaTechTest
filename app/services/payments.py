from app.schemas.payments import AddRequestPayment
from app.services.accounts import AccountService
from app.services.base import BaseService


class PaymentService(BaseService):
    async def create_transaction(self, data: AddRequestPayment, user__id: int):
        account = await AccountService(self.db).get_account_by_user(data.account_id, user__id)
        if not account:
            raise Exception
        await self.db.accounts.make_payment(data)
        await self.db.payments.add(data)
        await self.db.commit()
        
    async def get_transactions_history(self, user_id: int):
        accounts = await AccountService(self.db).get_accounts(user_id)
        accounts_ids = [account.id for account in accounts]
        transactions = await self.db.payments.transactions_history(accounts_ids)
        return transactions