from fastapi import APIRouter, Depends, status, HTTPException, Response,Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from smartQ import token, database
from smartQ.hashing import Hash

router = APIRouter(tags=['Authentication'])

templates = Jinja2Templates(directory="frontend")

# Get Home Pages
@router.get("/")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/login.html", context)

@router.post('/login')
def login(response: Response, request: OAuth2PasswordRequestForm = Depends()):
    user = database.find_user(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user["email"]})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/signin")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/signin.html", context)

@router.get("/menu")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/menu.html", context)

@router.get("/menu/device")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/device.html", context)

@router.get("/menu/inference")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/inference.html", context)

@router.get("/menu/result")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/result.html", context)

@router.get("/menu/model")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/model.html", context)