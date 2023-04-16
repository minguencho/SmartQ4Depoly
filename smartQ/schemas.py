from typing import Optional, List
from pydantic import BaseModel



class User(BaseModel):
    email:str
    password:str


class ShowUser(BaseModel):
    email:str
    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Device(BaseModel):
    email: str
    device_name: str

class Group(BaseModel):
    email: str
    group_name: str
    device_names: Optional[List] = None