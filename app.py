from fastapi import FastAPI

from smartQ.routers import authentication, user, device, model, inference, search, menu, group


app = FastAPI()
      

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(device.router)
app.include_router(model.router)
app.include_router(inference.router)
app.include_router(search.router)
app.include_router(menu.router)
app.include_router(group.router)

