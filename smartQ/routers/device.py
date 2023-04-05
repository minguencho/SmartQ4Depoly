from fastapi import APIRouter, Depends, status, HTTPException

from smartQ import schemas, oauth2, database

router = APIRouter(
    prefix="/device",
    tags=['device']
)



@router.post('/register', status_code=status.HTTP_200_OK)
def device_register(get_device: schemas.GetDevice, current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    device = schemas.Device(email=current_user.email, device_name=get_device.device_name)
    if database.check_device(device.email, device.device_name):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="Device name is already exist")
    
    database.insert_device(device)
    
    return f"{device.email} User's {device.device_name} Device created"