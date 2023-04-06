from fastapi import APIRouter, status, HTTPException, Request

from smartQ import schemas, hashing, database, rabbitmq
from fastapi.templating import Jinja2Templates
router = APIRouter(
    prefix="/user",
    tags=['Users']
)

templates = Jinja2Templates(directory="frontend")

@router.get("/signin")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/signin.html", context)


@router.post('/signin')
def create_user(request: schemas.User):
    new_user = schemas.User(email=request.email, password=hashing.Hash.bcrypt(request.password))
    print(new_user)
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