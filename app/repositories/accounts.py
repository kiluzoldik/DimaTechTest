from sqlalchemy import insert, select, update
from app.models.accounts import AccountsORM
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import AcountDataMapper
from app.schemas.accounts import Account, AddAccount
from app.schemas.payments import AddRequestPayment


class AccountsRepository(BaseRepository):
    model = AccountsORM
    mapper = AcountDataMapper

    async def get_accounts_by_user(self, user_id: int) -> list[Account]:
        query = select(self.model).filter_by(user_id=user_id)
        result = await self.session.execute(query)
        accounts = [self.mapper.map_to_domain_entity(account) for account in result.scalars().all()]
        return accounts

    async def add_account_for_user(self, user_id: int):
        account = AddAccount(user_id=user_id)
        query = insert(self.model).values(**account.model_dump())
        await self.session.execute(query)
        
    async def make_payment(self, data: AddRequestPayment):
        query = (
            update(self.model)
            .where(self.model.id == data.account_id)
            .values(balance=self.model.balance + data.amount)
        )
        await self.session.execute(query)
        