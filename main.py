from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.controllers.user_controller import router as user_controller

from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from controllers import auth_controller  # ✅ your auth controller

app = FastAPI()

# Optional: CORS (allowing frontend to call backend APIs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (if you have any CSS/JS in `static/` folder)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates (already used in your controllers)
templates = Jinja2Templates(directory="templates")

# Include your controller/router
app.include_router(auth_controller.router)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_controller.router)
