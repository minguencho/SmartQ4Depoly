from fastapi import FastAPI

from smartQ import rabbitmq
from smartQ.routers import authentication, user, device, model, inference, search, menu

app = FastAPI()

Mongo = rabbitmq.Result_Saver()

"""@app.on_event("startup")
def startup_Result_Saver():
    
    Mongo.consume()
    
@app.on_event("shutdown")
def shutdown_Result_Saver():
    Mongo.stop_consume()
"""
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(device.router)
app.include_router(model.router)
app.include_router(inference.router)
app.include_router(search.router)
app.include_router(menu.router)

