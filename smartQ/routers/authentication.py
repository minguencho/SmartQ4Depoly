from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

from smartQ import token
from smartQ.hashing import Hash

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(db: Request, request: OAuth2PasswordRequestForm = Depends()):
    user = db.app.database["Users"].find_one({"email": request.username})
    user['_id'] = str(user['_id'])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}