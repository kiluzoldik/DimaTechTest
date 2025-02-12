from hashlib import sha256

from app.exceptions import SignatureValidationException
from app.schemas.payments import AddRequestPayment
from app.config import settings


def check_transaction_signature(user_id: int, data: AddRequestPayment):
    result_string = f"{data.account_id}{data.amount}{data.transaction_id}{user_id}{settings.SECRET_PAYMENT_KEY}"
    my_signature = sha256(result_string.encode("utf-8")).hexdigest()
    if my_signature != data.signature:
        raise SignatureValidationException
    