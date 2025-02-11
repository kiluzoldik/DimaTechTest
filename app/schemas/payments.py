from pydantic import BaseModel


class AddRequestPayment(BaseModel):
    transaction_id: int
    amount: float
    account_id: int
    
    
class Payment(AddRequestPayment):
    id: int
