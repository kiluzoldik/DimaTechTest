from app.exceptions import AccountNotFoundException, DeleteAccountBalanceNotNullException, ObjectNotFoundException
from app.schemas.accounts import Account
from app.services.base import BaseService


class AccountService(BaseService):
    async def get_account_by_user(self, account_id: int, user_id: int):
        account = await self.db.accounts.get_one_or_none(id=account_id, user_id=user_id)
        return account
    
    async def get_accounts(self, user_id: int) -> list[Account]:
        accounts = await self.db.accounts.get_accounts_by_user(user_id)
        return accounts
    
    async def create_account(self, user_id: int):
        account = await self.db.accounts.add_account_for_user(user_id)
        await self.db.commit()
        return account
    
    async def delete_account(self, account_id: int, user_id: int):
        account = await self.get_account_by_user(account_id, user_id)
        if not account:
            raise AccountNotFoundException
        if account.balance != 0:
            raise DeleteAccountBalanceNotNullException
        
        await self.db.accounts.delete(id=account_id, user_id=user_id)
        await self.db.commit()
        
        