from fastapi import APIRouter, Depends, status, HTTPException

from smartQ import schemas, oauth2, utils, database

router = APIRouter(
    prefix="/inference",
    tags=['inference']
)

"""
추론
request : current_user, img_file, list(model name), list(device_name)
response : None, just do inference
"""

@router.post('/inference', status_code=status.HTTP_200_OK)
def inference(inf_data: schemas.InferenceData, current_user: schemas.User = Depends(oauth2.get_current_user)):
    user_email = current_user.email
    image_msg = utils.img2msg(inf_data.image)
    models = database.get_models(current_user.email, inf_data.model_names)
    models_msg = utils.models2msg(models)
    msgs = image_msg + models_msg
    
    routing_keys = utils.make_routing_key(inf_data.device_names)
    
    utils.publish_inference_message(msgs, user_email, routing_keys)
        
    return True
