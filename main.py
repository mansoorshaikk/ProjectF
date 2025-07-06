from src.controllers.user_controller import router as auth_router
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.include_router(auth_router.router)
