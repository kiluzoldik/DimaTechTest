from pydantic import BaseModel


class AddAccount(BaseModel):
    balance: float = 0
    user_id: int
    

class Account(AddAccount):
    id: int