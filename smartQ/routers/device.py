from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from smartQ import schemas, database, token

router = APIRouter(
    prefix="/device",
    tags=['device']
)

templates = Jinja2Templates(directory="frontend")

@router.get('/')
def device_page(request: Request):
    
    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            errors.append("You have to Login first")
            return templates.TemplateResponse("/device.html", {'request': request, 'errors': errors})
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                errors.append("Re Login Please")
                return templates.TemplateResponse("/device.html", {'request': request, 'errors': errors})
            else:
                device_names = database.get_device_names(user_email)
                return templates.TemplateResponse("/device.html", {'request': request, 'device_names' : device_names})
    except:
        errors.append("Something Wrong. Please Try Again")
        return templates.TemplateResponse("/device.html", {'request': request, 'errors': errors})    


@router.post('/register', status_code=status.HTTP_200_OK)
async def device_register(request: Request):
    form = await request.form()
    device_name = form.get("device_name")

    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
           return RedirectResponse('/device/',status_code=302)
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                return RedirectResponse('/device/',status_code=302)
            else:
                device = schemas.Device(email=user_email, device_name=device_name)
                if database.check_device(device.email, device.device_name):
                    errors.append(f"You already have device name [{device_name}]")
                    return RedirectResponse('/device/',status_code=302)
                else:
                    database.insert_device(device)
                    return RedirectResponse('/device/',status_code=302)
                    
    except:
        return RedirectResponse('/device/',status_code=302)

