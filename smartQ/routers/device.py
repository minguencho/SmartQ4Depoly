from fastapi import APIRouter, Depends, status, HTTPException

from smartQ import schemas, oauth2, utils, database

router = APIRouter(
    prefix="/device",
    tags=['device']
)



@router.post('/register', status_code=status.HTTP_200_OK)
def device_register(device_name: str, current_user: schemas.User = Depends(oauth2.get_current_user)):
    
    device = schemas.Device(current_user.email, device_name)
    if database.check_device(device.email, device.device_name):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="Device name is already exist")
    
    database.insert_user(device)
    
    return f"{device.email} User's {device.device_name} Device created"
