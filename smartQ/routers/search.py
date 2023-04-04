from fastapi import APIRouter, Depends, status, HTTPException

from smartQ import schemas, oauth2, utils, database

router = APIRouter(
    prefix="/search",
    tags=['search']
)



@router.post('/device_register', status_code=status.HTTP_200_OK)
def search_all(device_name: str, current_user: schemas.User = Depends(oauth2.get_current_user)):
    

    return "search"
