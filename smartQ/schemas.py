from typing import List, Optional
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True


class User(BaseModel):
    email:str
    password:str


class ShowUser(BaseModel):
    email:str
    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body:str

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
    
    
class Blogs(BaseModel):
    __tablename__ = 'blogs'

    id: Optional[int]
    title: str
    body: str
    # user_id = Column(Integer, ForeignKey('users.id'))

    # creator = relationship("User", back_populates="blogs")


class Users(BaseModel):
    __tablename__ = 'users'

    id: Optional[int]
    email: str
    password: str

    # blogs = relationship('Blog', back_populates="creator")