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
    
    
class Device(BaseModel):
    email: str
    device_name: str


class GetMyModel(BaseModel):
    onnx: str
    my_model_name: str
    

class MyModel(BaseModel):
    email: str
    onnx: str
    my_model_name: str