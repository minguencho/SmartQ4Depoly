<<<<<<< HEAD
from fastapi import APIRouter, Request, Form, Response
=======
from fastapi import APIRouter, Request

>>>>>>> 6992e1fd2f291d3e1471a59d85f52fcf08a76060
from smartQ import schemas, hashing, database, rabbitmq
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
router = APIRouter(tags=['login'])

templates = Jinja2Templates(directory="frontend")

@router.get("/signin")
<<<<<<< HEAD
async def signin(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/signin.html", context)
=======
async def home_page(request: Request):
    return templates.TemplateResponse("/signin.html", {'request': request})
>>>>>>> 6992e1fd2f291d3e1471a59d85f52fcf08a76060

@router.get("/")
async def tologin(request : Request):
    context  = {'request': request}
    return templates.TemplateResponse("/login.html", context)

@router.post('/signin')
async def create_user(request: Request, response : Response):
    
    form = await request.form()
    email = form.get("user_id")
    password = form.get("password")

    new_user = schemas.User(email = email, password=hashing.Hash.bcrypt(password))

<<<<<<< HEAD
    if database.check_user(new_user.email):
        error = "This id is already used, try other ID"
        print(error)
        return templates.TemplateResponse("signin.html",{"request" : request, "error" : error})
        #raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="User email is already exist")
    else:
        msg = "Register Successful " 
        print(msg)
        database.insert_user(new_user)
        rabbitmq.make_exchange(new_user.email)
        context = {'request' : request, 'success' : True}
        return templates.TemplateResponse("login.html", context)
=======
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


>>>>>>> 6992e1fd2f291d3e1471a59d85f52fcf08a76060
"""
@router.get('/get/{email}')
def get_user(email: str):
    user = database.find_user(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with the id ? is not available")
    
    return user
"""