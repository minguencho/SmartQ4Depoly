from fastapi import APIRouter
from fastapi import APIRouter, status, HTTPException, Request

from smartQ import schemas, hashing


router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post('/')
def create_user(db: Request, request: schemas.User):
    new_user = schemas.User(email=request.email, password=hashing.Hash.bcrypt(request.password))
    dict_new_user = dict(new_user)
    print(dict_new_user)
    db.app.database["Users"].insert_one(dict_new_user)
    return new_user


@router.get('/get')
def get_user(db: Request):
    user = db.app.database["Users"].find_one()
    user['_id'] = str(user['_id'])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with the id ? is not available")
    
    return user