from pydantic import BaseModel, field_validator

from app.exceptions import DigitPasswordHTTPException, FullNameLengthHTTPException, FullNameValidationHTTPException, LengthPasswordHTTPException, SpecialSimbolPasswordHTTPException, UpperLetterPasswordHTTPException


class AddRequestUser(BaseModel):
    full_name: str
    email: str
    password: str
    
    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value: str):
        if len(value) < 10:
            raise FullNameLengthHTTPException
        if any(v.isdigit() for v in value):
            raise FullNameValidationHTTPException
        return value
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise LengthPasswordHTTPException
        if not any(c.isdigit() for c in value):
            raise DigitPasswordHTTPException
        if not any(c.isupper() for c in value):
            raise UpperLetterPasswordHTTPException
        if not any(c in "!@#$%^&*()-_=+[]{};:,.<>?/|" for c in value):
            raise SpecialSimbolPasswordHTTPException
        return value
    
    
class LoginUserRequest(BaseModel):
    email: str
    password: str
    
    
class AddUser(BaseModel):
    full_name: str
    email: str
    hashed_password: str
    
    
class FullEditUser(BaseModel):
    full_name: str
    email: str
    
    
class PartialEditUser(BaseModel):
    full_name: str | None = None
    email: str | None = None
    

class User(FullEditUser):
    id: int
    
    
class FullUser(User):
    is_admin: bool = False    
    
    
class UserWithHashedPassword(User):
    hashed_password: str
