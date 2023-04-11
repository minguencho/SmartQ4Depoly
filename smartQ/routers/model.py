from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates

from smartQ import schemas, utils, database, token
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
    get_model = await request.body()
    get_model = json.loads(get_model.decode('utf-8'))
    my_model_name = get_model['custom_model_name']
    my_model_contents = get_model['onnx']
    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            errors.append("You have to Login first")
            return templates.TemplateResponse("/model.html", {'request': request, 'errors': errors})
        else:
            print('1')
            user_email = token.verify_token(access_token)
            print(user_email)
            onnx_contents = utils.extract_onnx(my_model_contents)
            print(type(onnx_contents))
            # onnx_contents = get_model.onnx # for testing
            model = schemas.Model(email=user_email, onnx=onnx_contents, model_name=my_model_name)
            print(model.email)
            if database.check_model(model.email, model.model_name):
                print('3')
                errors.append("Input Model name is already exists")
                return templates.TemplateResponse("/model.html", {'request': request, 'errors': errors})
            else:
                print('2')
                database.insert_model(model)
                print('success')
                msg = f"[{model.model_name}] Reigster successfully"
                return templates.TemplateResponse("/model.html", {'request': request, 'msg': msg})

    except:
        errors.append("Something Wrong. Please Try Again")
        return templates.TemplateResponse("/model.html", {'request': request, 'errors': errors})


