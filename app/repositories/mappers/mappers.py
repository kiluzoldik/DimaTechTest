from app.models.users import UsersORM
from app.repositories.mappers.base import DataMapper
from app.schemas.users import User, UserWithHashedPassword


class UserDataMapper(DataMapper):
    model = UsersORM
    schema = User
    

class UserWithHashedPasswordDataMapper(DataMapper):
    model = UsersORM
    schema = UserWithHashedPassword