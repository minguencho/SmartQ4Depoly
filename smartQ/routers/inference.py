from fastapi import APIRouter, status, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from smartQ import utils, token, rabbitmq, database

router = APIRouter(
    prefix="/inference",
    tags=['inference']
)

templates = Jinja2Templates(directory="frontend")

"""
추론
request : current_user, img_file, list(model name), list(device_name)
response : None, just do inference
"""

@router.get('/')
def inference_page(request: Request):

    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            errors.append("You have to Login first")
            return templates.TemplateResponse("/inference.html", {'request': request, 'errors': errors})
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                errors.append("Re Login Please")
                return templates.TemplateResponse("/inference.html", {'request': request, 'errors': errors})
            else:
                # device_names = rabbitmq.get_device_name(user_email)
                device_names = database.get_device_names(user_email)
                group_names = database.get_group_names(user_email)
                if not device_names:
                    errors.append("Go to Device page and register your device first !")
                    return templates.TemplateResponse("/inference.html", {'request': request, 'errors': errors})
                else:
                    model_names = utils.get_model_name(user_email)
                    context = {'request': request, 'model_names': model_names, 'device_names': device_names, 'group_names': group_names}
                    return templates.TemplateResponse("/inference.html", context)

    except:
        errors.append("Something Wrong. Please Try Again")
        return templates.TemplateResponse("/inference.html", {'request': request, 'errors': errors})


@router.post('/inference_request', status_code=status.HTTP_200_OK)
async def inference_request(request: Request):
    form = await request.form()
    image = form['image_file'].file.read()
    model_names = form.getlist('model_names')
    device_names = form.getlist('device_names')
    group_names = form.getlist('group_names')
    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            return RedirectResponse(f'/inference/', status_code=302)
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                return RedirectResponse(f'/inference/', status_code=302)
            else:
                image_msg = utils.img2msg(image)
                model_list = utils.get_onnx_file(user_email, model_names)
                models_msg = utils.model_list2msg(model_list)
                msgs = image_msg + models_msg
                group_devices = database.get_device_from_group(user_email, group_names)
                device_names += group_devices
                routing_keys = utils.make_routing_key(device_names)
                utils.publish_inference_message(msgs, user_email, routing_keys)
                return RedirectResponse(f'/inference/', status_code=302)

    except:
        errors.append("Something Wrong. Please Try Again")
        return RedirectResponse(f'/inference/', status_code=302)
