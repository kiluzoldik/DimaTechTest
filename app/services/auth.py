from datetime import datetime, timedelta, timezone

from fastapi import Response
import jwt
from passlib.context import CryptContext

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
        hashed_password = AuthService().get_password_hash(data.password)
        new_user_data = AddUser(
            full_name=data.full_name, 
            email=data.email, 
            hashed_password=hashed_password
        )
        await self.db.users.add(new_user_data)
        await self.db.commit()
        
    async def login(self, data: AddRequestUser, response: Response):
        user = await self.db.users.get_user_with_hashed_password(data.email)
        if not self.verify_password(data.password, user.hashed_password):
            raise Exception
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return access_token
        
    async def get_me(self, user_id):
        data = await self.db.users.get_one_or_none(id=user_id)
        user = User(full_name=data.full_name, email=data.email, id=data.id)
        if not user:
            raise Exception
        return user
    
    async def logout(self, response: Response):
        response.delete_cookie("access_token")