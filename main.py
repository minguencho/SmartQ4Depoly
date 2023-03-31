
from fastapi import FastAPI
from pymongo import MongoClient
from smartQ.routers import smartQ, user, authentication

app = FastAPI()

client = "mongodb+srv://bmk802:ahdrhelqlqlqjs1!@smartq.gan6cow.mongodb.net/?retryWrites=true&w=majority"
db = "smartQ"


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(client)
    app.database = app.mongodb_client[db]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(authentication.router)
app.include_router(smartQ.router)
app.include_router(user.router)