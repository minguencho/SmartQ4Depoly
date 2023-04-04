from fastapi import APIRouter, Depends, status, HTTPException

from smartQ import schemas, oauth2, utils, database

router = APIRouter(
    prefix="/model",
    tags=['model']
)


@router.post('/register', status_code=status.HTTP_200_OK)
def model_register(get_my_model: schemas.GetMyModel, current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    onnx_contents = utils.extract_onnx(get_my_model.onnx)
    my_model = schemas.MyModel(current_user.email, onnx_contents, get_my_model.my_model_name)
    if database.check_my_model(my_model.email, my_model.my_model_name):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"{my_model.my_model_name} is already exist")
    
    database.insert_my_model(my_model)
    
    return f"{my_model.email} User's {my_model.my_model_name} Model saved"


