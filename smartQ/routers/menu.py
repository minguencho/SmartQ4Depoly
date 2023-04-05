from fastapi import APIRouter

router = APIRouter(
    prefix='/menu',
    tags=['Authentication']
    )


@router.post('/login')
def login():
    return True