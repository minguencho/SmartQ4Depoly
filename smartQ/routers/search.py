from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.templating import Jinja2Templates
from smartQ import schemas, oauth2, utils, database

router = APIRouter(
    prefix="/result",
    tags=['result']
)

templates = Jinja2Templates(directory="frontend")

@router.get('/')
def result_page(request: Request):
    return templates.TemplateResponse("/result.html", {'request': request})

@router.get('/insert', status_code=status.HTTP_200_OK)
def insert_test_data(current_user: schemas.User = Depends(oauth2.get_current_user)):
    test_dict = {"email": current_user.email, "inf_object": "dog", "accuracy": "95"}
    database.insert_test_data(test_dict)
    return f'{test_dict} inserted'


@router.get('/all', status_code=status.HTTP_200_OK)
def search_all(current_user: schemas.User = Depends(oauth2.get_current_user)):
    email = current_user.email
    results = database.get_results(email)
    if not results:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Any results in your database")
    results_list = utils.result_to_list(results)
    
    return results_list
