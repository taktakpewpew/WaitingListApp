from fastapi import FastAPI
from app.api.routes import user, waiting_list
from app.exceptions.handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)
app.include_router(waiting_list.router, prefix="/waiting-list", tags=["WaitingList"])
app.include_router(user.router, prefix="/users", tags=["Users"])