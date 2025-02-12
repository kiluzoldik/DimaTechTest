from sqlalchemy import select
from app.models.payments import PaymentsORM
from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import PaymentDataMapper


class PaymentsRepository(BaseRepository):
    model = PaymentsORM
    mapper = PaymentDataMapper
    
    async def transactions_history(self, accounts_ids: list[int]):
        query = (
            select(self.model)
            .filter(self.model.account_id.in_(accounts_ids))
        )
        result = await self.session.execute(query)
        transactions = [
            self.mapper.map_to_domain_entity(object) for object in result.scalars().all()
        ]
        return transactions
