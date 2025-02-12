from datetime import datetime, timedelta, timezone

from fastapi import Response
import jwt
from passlib.context import CryptContext
from validate_email_address import validate_email

from app.exceptions import EmailException, EmailPasswordValidationException, ObjectAlreadyExistsException, UserEmailAlreadyExistsException, UserEmailNotFoundException, UserNotFoundException
from app.schemas.users import AddRequestUser, AddUser, User
from app.services.base import BaseService
from app.config import settings


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> str:
        try:
            return jwt.decode(
                token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except Exception:
            raise Exception
    
    async def register(self, data: AddRequestUser):
        is_valid = validate_email(data.email, verify=True)
        if not is_valid:
            raise EmailException
        hashed_password = AuthService().get_password_hash(data.password)
        new_user_data = AddUser(
            full_name=data.full_name, 
            email=data.email, 
            hashed_password=hashed_password
        )
        try:
            await self.db.users.add(new_user_data)
        except ObjectAlreadyExistsException:
            raise UserEmailAlreadyExistsException
        
        await self.db.commit()
        
    async def login(self, data: AddRequestUser, response: Response):
        try:
            user = await self.db.users.get_user_with_hashed_password(data.email)
        except UserEmailNotFoundException:
            raise UserEmailNotFoundException
        
        if not self.verify_password(data.password, user.hashed_password):
            raise EmailPasswordValidationException
        
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token
        
    async def get_me(self, user_id: int):
        data = await self.db.users.get_one_or_none(id=user_id)
        if not data:
            raise UserNotFoundException
        user = User(full_name=data.full_name, email=data.email, id=data.id)
        return user
    
    async def logout(self, response: Response):
        response.delete_cookie("access_token")
        
    async def admin_required(self, user_id: int):
        return await self.db.users.check_admin(user_id)
