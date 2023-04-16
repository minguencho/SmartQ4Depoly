from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from smartQ import schemas, database, token

router = APIRouter(
    prefix="/group",
    tags=['group']
)

templates = Jinja2Templates(directory="frontend")


@router.get('/')
def group_page(request: Request):

    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            errors.append("You have to Login first")
            return templates.TemplateResponse("/group.html", {'request': request, 'errors': errors})
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                errors.append("Re Login Please")
                return templates.TemplateResponse("/group.html", {'request': request, 'errors': errors})
            else:
                device_names = database.get_device_names(user_email)
                group_dict = database.get_group_dict_list(user_email)
                context = {'request': request, 'device_names': device_names}
                context.update(group_dict)
                return templates.TemplateResponse("/group.html", context)
    except:
        errors.append("Something Wrong. Please Try Again")
        return templates.TemplateResponse("/group.html", {'request': request, 'errors': errors})    


@router.post('/register', status_code=status.HTTP_200_OK)
async def group_register(request: Request):
    form = await request.form()
    group_name = form.get("group_name")

    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
           return RedirectResponse('/group/',status_code=302)
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                return RedirectResponse('/group/',status_code=302)
            else:
                group = schemas.Group(email=user_email, group_name=group_name)
                if database.check_group(group.email, group.group_name):
                    errors.append(f"You already have group name [{group_name}]")
                    return RedirectResponse('/group/',status_code=302)
                else:
                    database.insert_group(group)
                    return RedirectResponse('/group/',status_code=302)
                    
    except:
        return RedirectResponse('/group/',status_code=302)


@router.post('/device2group', status_code=status.HTTP_200_OK)
async def device2group(request: Request):
    form = await request.form()
    device_names = form.getlist('device_names')
    group_name = form.get('group_name')
    print(device_names)

    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
           return RedirectResponse('/group/',status_code=302)
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                return RedirectResponse('/group/',status_code=302)
            else:
                group = schemas.Group(email=user_email, group_name=group_name)
                if not database.check_group(group.email, group.group_name):
                    errors.append(f"You don't have group name [{group_name}]")
                    return RedirectResponse('/group/',status_code=302)
                else:
                    database.insert_device2group(user_email, group_name, device_names)
                    return RedirectResponse('/group/',status_code=302)
                    
    except:
        return RedirectResponse('/group/',status_code=302)
