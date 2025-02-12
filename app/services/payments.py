from app.exceptions import ObjectAlreadyExistsException, SignatureValidationException, TransactionIdAlreadyExistsException
from app.schemas.payments import AddPayment, AddRequestPayment
from app.services.accounts import AccountService
from app.services.base import BaseService
from app.services.utils import check_transaction_signature


class PaymentService(BaseService):
    async def create_transaction(self, data: AddRequestPayment, user_id: int):
        try:
            check_transaction_signature(user_id, data)
        except SignatureValidationException:
            raise SignatureValidationException
        
        account = await AccountService(self.db).get_account_by_user(data.account_id, user_id)
        if not account:
            await AccountService(self.db).create_account(user_id)
        new_data = AddPayment(
            transaction_id=data.transaction_id,
            amount=data.amount,
            account_id=data.account_id
        )
        try:
            await self.db.accounts.make_payment(new_data)
            await self.db.payments.add(new_data)
        except ObjectAlreadyExistsException:
            raise TransactionIdAlreadyExistsException
        await self.db.commit()
        
    async def get_transactions_history(self, user_id: int) -> list:
        accounts = await AccountService(self.db).get_accounts(user_id)
        accounts_ids = [account.id for account in accounts]
        transactions = await self.db.payments.transactions_history(accounts_ids)
        return transactions
