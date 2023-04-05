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

@router.get("/device")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/device.html", context)

@router.get("/inference")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/inference.html", context)

@router.get("/result")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/result.html", context)

@router.get("/model")
async def home_page(request : Request):
    context = {'request': request}
    return templates.TemplateResponse("/model.html", context)