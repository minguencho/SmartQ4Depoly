from fastapi import APIRouter, Depends, status, HTTPException

from smartQ import schemas, oauth2, utils, database

router = APIRouter(
    prefix="/smartQ",
    tags=['SmartQ']
)



@router.post('/device_register', status_code=status.HTTP_200_OK)
def device_register(device_name: str, current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    device = schemas.Device(current_user.email, device_name)
    if database.check_device(device.email, device.device_name):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="Device name is already exist")
    
    database.insert_user(device)
    
    return f"{device.email} User's {device.device_name} Device created"



@router.post('/my_model_register', status_code=status.HTTP_200_OK)
def my_model_register(get_my_model: schemas.GetMyModel, current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    onnx_contents = utils.extract_onnx(get_my_model.onnx)
    my_model = schemas.MyModel(current_user.email, onnx_contents, get_my_model.my_model_name)
    if database.check_my_model(my_model.email, my_model.my_model_name):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"{my_model.my_model_name} is already exist")
    
    database.insert_my_model(my_model)
    
    return f"{my_model.email} User's {my_model.my_model_name} Model saved"




"""
추론
request : current_user, img_file, list(model name), list(device_name)
response : None, just do inference
"""

@router.post('/inference', status_code=status.HTTP_200_OK)
def inference(inf_data: schemas.InferenceData, current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    image_msg = utils.img2msg(inf_data.image)
    models = database.get_models(current_user.email, inf_data.model_names)
    models_msg = utils.models2msg(models)
    msgs = image_msg + models_msg
    
    routing_keys = utils.make_routing_key(inf_data.device_names)
    
    utils.publish_inference_message(msgs, routing_keys)
        
    return True
