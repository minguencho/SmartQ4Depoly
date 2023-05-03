from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/menu',
    tags=['Authentication']
    )

templates = Jinja2Templates(directory="frontend")

@router.get("/")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/menu.html", context)