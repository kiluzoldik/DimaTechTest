from pydantic import BaseModel

from app.schemas.payments import Payment


class AddAccount(BaseModel):
    balance: int = 0
    user_id: int
    

class Account(AddAccount):
    id: int
    
    
class AccountWithPayments(Account):
    transactions: list[Payment] = []