from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates

from smartQ import utils, token
import json

router = APIRouter(
    prefix="/model",
    tags=['model']
)

templates = Jinja2Templates(directory="frontend")


@router.get('/')
def device_page(request: Request):
    return templates.TemplateResponse("/model.html", {'request': request})
    

@router.post('/register', status_code=status.HTTP_200_OK)
async def model_register(request: Request):
    form = await request.form()
    model_name = f"{form.get('custom_model_name')}.onnx"
    model = form['onnx'].file.read()
    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            errors.append("You have to Login first")
            return templates.TemplateResponse("/model.html", {'request': request, 'errors': errors})
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                errors.append("Re Login Please")
                return templates.TemplateResponse("/model.html", {'request': request, 'errors': errors})
            else:
                if utils.check_model(user_email, model_name):
                    errors.append(f"[{model_name}] Model name is already exists")
                    return templates.TemplateResponse("/model.html", {'request': request, 'errors': errors})
                else:
                    utils.write_onnx(user_email, model_name, model)
                    msg = f"[{model_name}] Reigster successfully"
                    return templates.TemplateResponse("/model.html", {'request': request, 'msg': msg})

    except:
        errors.append("Something Wrong. Please Try Again")
        return templates.TemplateResponse("/model.html", {'request': request, 'errors': errors})
    