from app.repositories.accounts import AccountsRepository
from app.repositories.payments import PaymentsRepository
from app.repositories.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        
    async def __aenter__(self):
        self.session = self.session_factory()
        
        self.users = UsersRepository(self.session)
        self.accounts = AccountsRepository(self.session)
        self.payments = PaymentsRepository(self.session)
        
        return self
    
    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()
        
    async def commit(self):
        await self.session.commit()