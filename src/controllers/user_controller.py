from fastapi import APIRouter, Request, Form,status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from src.utils.auth import get_logged_in_user
from ..services.user_service import UserService



router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def get_signup(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


@router.get("/signup")
def get_signup(request:Request):
    return templates.TemplateResponse("signup.html",{"request":request})

@router.get("/login")
def get_login(request:Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/api/signup")
def make_signup(request:Request,email:str =Form(...),password:str = Form(...)):
    try:
        user_service = UserService()
        res = user_service.signup_user(email, password)
        if res:
            response = RedirectResponse(
                url="/login",
                status_code=status.HTTP_303_SEE_OTHER)
            return response
        else:
            return templates.TemplateResponse("signup.html", {"request": request, "error": "Signup failed."})
    except Exception as e:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Signup failed."})


@router.post("/api/login")
def make_login(request:Request,email:str =Form(...),password:str = Form(...)):
    try:
        user_service = UserService()
        res = user_service.login_user(email, password)
        if res:
            response = RedirectResponse(
                url="/dashboard",
                status_code=status.HTTP_303_SEE_OTHER)
            return response
        else:
            return templates.TemplateResponse("login.html", {"request": request, "error": "login failed."})
    except Exception as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": "login failed."})


@router.get("/dashboard")
def get_dashboard(request:Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

