from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates

from smartQ import schemas, database, token

router = APIRouter(
    prefix="/device",
    tags=['device']
)

templates = Jinja2Templates(directory="frontend")


@router.get('/')
def device_page(request: Request):
    return templates.TemplateResponse("/device.html", {'request': request})
    

@router.post('/', status_code=status.HTTP_200_OK)
async def device_register(request: Request):
    form = await request.form()
    device_name = form.get("device_name")

    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            errors.append("You have to Login first")
            return templates.TemplateResponse("/device.html", {'request': request, 'errors': errors})
        else:
            user_email = token.verify_token(access_token)
            device = schemas.Device(email=user_email, device_name=device_name)
            if database.check_device(device.email, device.device_name):
                errors.append(f"You already have device name [{device_name}]")
                return templates.TemplateResponse("/device.html", {'request': request, 'errors': errors})
            else:
                database.insert_device(device)
                msg = f"[{device_name}] Register successfully"
                return templates.TemplateResponse("/device.html", {'request': request, 'msg': msg})
    
    except:
        errors.append("Something Wrong. Please Try Again")
        return templates.TemplateResponse("/device.html", {'request': request, 'errors': errors})
