from pydantic import BaseModel


class AddRequestUser(BaseModel):
    full_name: str
    email: str
    password: str
    
    
class AddUser(BaseModel):
    full_name: str
    email: str
    hashed_password: str
    
    
class EditUser(BaseModel):
    full_name: str
    email: str
    

class User(EditUser):
    id: int
    
    
class UserWithHashedPassword(User):
    hashed_password: str
