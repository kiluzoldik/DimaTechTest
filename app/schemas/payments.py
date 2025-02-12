from pydantic import BaseModel


class AddRequestPayment(BaseModel):
    transaction_id: str
    amount: int
    account_id: int
    signature: str
    
    
class AddPayment(BaseModel):
    transaction_id: str
    amount: int
    account_id: int


class Payment(AddPayment):
    id: int