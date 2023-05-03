from fastapi import APIRouter, status, Request
from fastapi.templating import Jinja2Templates
from smartQ import database, token, database

router = APIRouter(
    prefix="/result",
    tags=['result']
)

templates = Jinja2Templates(directory="frontend")

@router.get('/')
def result_page(request: Request):
    
    return templates.TemplateResponse("/result.html", {'request': request})    


@router.get('/search', status_code=status.HTTP_200_OK)
async def result_search(request: Request, search: str = 'default', keyword: str = 'default'):
    
    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            errors.append("You have to Login first")
            return templates.TemplateResponse("/result.html", {'request': request, 'errors': errors})
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                errors.append("Re Login Please")
                return templates.TemplateResponse("/result.html", {'request': request, 'errors': errors})
            else:
                results = database.get_results(user_email, search, keyword)
                context = {'request': request}
                context.update(results)
                return templates.TemplateResponse("/result.html", context)
    except:
        errors.append("Something Wrong. Please Try Again")
        return templates.TemplateResponse("/result.html", {'request': request, 'errors': errors})    



@router.get('/delete_all', status_code=status.HTTP_200_OK)
def delete_all(request: Request):
    
    errors = []
    try:
        scheme,_,access_token = request.cookies.get("access_token").partition(" ")
        if access_token is None:
            errors.append("You have to Login first")
            return templates.TemplateResponse("/result.html", {'request': request, 'errors': errors})
        else:
            user_email = token.verify_token(access_token)
            if not user_email:
                errors.append("Re Login Please")
                return templates.TemplateResponse("/result.html", {'request': request, 'errors': errors})
            else:
                database.delete_all(user_email)
                context = {'request': request}
                return templates.TemplateResponse("/result.html", context)
    except:
        errors.append("Something Wrong. Please Try Again")
        return templates.TemplateResponse("/result.html", {'request': request, 'errors': errors})    
