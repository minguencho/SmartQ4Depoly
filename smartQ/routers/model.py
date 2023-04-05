from fastapi import APIRouter, Depends, status, HTTPException

from smartQ import schemas, oauth2, database

router = APIRouter(
    prefix="/model",
    tags=['model']
)


@router.post('/register', status_code=status.HTTP_200_OK)
def model_register(get_model: schemas.GetModel, current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    # onnx_contents = utils.extract_onnx(get_model.onnx)
    onnx_contents = get_model.onnx # for testing
    model = schemas.Model(email=current_user.email, onnx=onnx_contents, model_name=get_model.model_name)
    if database.check_model(model.email, model.model_name):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"{model.model_name} is already exist")
    
    database.insert_model(model)
    
    return f"{model.email} User's {model.model_name} Model saved"


