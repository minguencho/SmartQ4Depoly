from fastapi import APIRouter
from fastapi import APIRouter, status, HTTPException

from smartQ import schemas, hashing, database, rabbitmq


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post('/create')
def create_user(request: schemas.User):
    new_user = schemas.User(email=request.email, password=hashing.Hash.bcrypt(request.password))
    if database.check_user(new_user.email):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="User email is already exist")
    
    database.insert_user(new_user)
    rabbitmq.make_exchange(new_user.email)
    
    return f"{new_user.email} User created"

"""
@router.get('/get/{email}')
def get_user(email: str):
    user = database.find_user(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with the id ? is not available")
    
    return user
"""