from app.models.accounts import AccountsORM
from app.models.payments import PaymentsORM
from app.models.users import UsersORM
from app.repositories.mappers.base import DataMapper
from app.schemas.accounts import Account, AccountWithPayments
from app.schemas.payments import Payment
from app.schemas.users import FullUser, User, UserWithHashedPassword


class UserDataMapper(DataMapper):
    model = UsersORM
    schema = User
    

class UserWithHashedPasswordDataMapper(DataMapper):
    model = UsersORM
    schema = UserWithHashedPassword
    
    
class AcountDataMapper(DataMapper):
    model = AccountsORM
    schema = Account
    

class AccountWithPaymentsDataMapper(DataMapper):
    model = AccountsORM
    schema = AccountWithPayments
    
    
class PaymentDataMapper(DataMapper):
    model = PaymentsORM
    schema = Payment
    
    
class UserDataMapper(DataMapper):
    model = UsersORM
    schema = FullUser