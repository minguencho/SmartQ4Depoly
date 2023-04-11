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
    

class InferenceData(BaseModel):
    image: str
    model_names: List[str]
    device_names: List[str]
    
    
class GetDevice(BaseModel):
    device_name: str


class Device(GetDevice):
    email: str


class GetModel(BaseModel):
    onnx: str
    model_name: str
    

class Model(GetModel):
    email: str
    