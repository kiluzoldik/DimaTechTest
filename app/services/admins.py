from app.exceptions import ObjectNotFoundException, UserNotFoundException
from app.repositories.accounts import AccountsRepository
from app.schemas.users import FullEditUser, PartialEditUser
from app.services.auth import AuthService
from app.services.base import BaseService


class AdminService(BaseService):
    async def get_all_users(self):
        return await self.db.users.get_all()
        
    async def get_accounts_with_payments_by_user(self, user_id: int):
        user = await AuthService(self.db).get_me(user_id)
        if not user:
            raise UserNotFoundException
        
        return await AccountsRepository(self.db.session).transactions_history_for_accounts(user_id)
    
    async def partial_update_user(self, user_id: int, data: PartialEditUser):
        try:
            await AuthService(self.db).get_me(user_id)
            await self.db.users.edit(data=data, exclude_unset=True, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
        await self.db.commit()
        
    async def full_update_user(self, user_id: int, data: FullEditUser):
        try:
            await AuthService(self.db).get_me(user_id)
            await self.db.users.edit(data=data, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
            
        await self.db.commit()
        
    async def delete_user(self, user_id: int):
        try:
            await AuthService(self.db).get_me(user_id)
            await self.db.users.delete(id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException
            
        await self.db.commit()