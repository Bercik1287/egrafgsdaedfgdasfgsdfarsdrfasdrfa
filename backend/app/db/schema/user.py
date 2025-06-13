from pydantic import BaseModel
from typing import Union

class UserInCreate(BaseModel):
    username: str
    password: str

class UserOutput(BaseModel):
    id: int
    username: str
    
class UserInUpdate(BaseModel):
    id: int
    username: Union[str, None] = None
    password: Union[str, None] = None

class UserInLogin(BaseModel):
    username: str
    password: str

class UserWithToken(BaseModel):
    token: str