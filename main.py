from fastapi import FastAPI

from smartQ.routers import smartQ, user, authentication

app = FastAPI()


app.include_router(authentication.router)
app.include_router(smartQ.router)
app.include_router(user.router)