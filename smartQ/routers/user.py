from fastapi import APIRouter, Request

from smartQ import schemas, hashing, database, rabbitmq
from fastapi.templating import Jinja2Templates
router = APIRouter(
    prefix="/user",
    tags=['Users']
)

templates = Jinja2Templates(directory="frontend")

@router.get("/signin")
async def home_page(request: Request):
    return templates.TemplateResponse("/signin.html", {'request': request})


@router.post('/signin')
async def create_user(request: Request):
    form = await request.form()
    user_email = form.get("user_email")
    password = form.get("password")
    
    errors = []
    if not user_email:
        errors.append("Please Enter Email")
    if not password:
        errors.append("Please Enter Password ")
    
    try:
        new_user = schemas.User(email=user_email, password=hashing.Hash.bcrypt(password))
        if database.check_user(new_user.email):
            errors.append("Email already exists")
            return templates.TemplateResponse("signin.html", {"request": request, "errors": errors})
        else:
            database.insert_user(new_user)
            rabbitmq.make_exchange(new_user.email)
            msg = "User created"
            return templates.TemplateResponse("signin.html", {"request": request, "msg": msg})
 
    except:
        errors.append("Something Wrong")
        return templates.TemplateResponse("signin.html", {"request": request, "errors": errors})


"""
@router.get('/get/{email}')
def get_user(email: str):
    user = database.find_user(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with the id ? is not available")
    
    return user
"""