from fastapi import APIRouter, Request, Form,status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from src.utils.auth import get_logged_in_user
from ..services.user_service import UserService



router = APIRouter()
templates = Jinja2Templates(directory="templates")

def logged_user(request:Request):
    session_token = request.cookies.get('user_session')
    user_service = UserService()
    user = user_service.current_user(session_token)
    if user:
        return user
    else:
        return None

@router.get("/")
def get_homepage(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


@router.get("/signup")
def get_signup(request:Request):
    user = logged_user(request)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/login")
def get_login(request:Request):
    user = logged_user(request)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
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
        if res and res.session and res.session.access_token:
            response = RedirectResponse(
                url="/dashboard",
                status_code=status.HTTP_303_SEE_OTHER
            )
            response.set_cookie(
                key="user_session",
                value=res.session.access_token,
                httponly=True,
                secure=True,  # only use secure=True if you're serving over HTTPS
                samesite='lax',
                max_age=3600
            )
            return response
        else:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    except Exception as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": "login failed."})


@router.get("/dashboard")
def get_dashboard(request:Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

