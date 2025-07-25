from fastapi import APIRouter, Request, Form, status, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from src.utils.auth import get_logged_in_user
from ..services.user_service import UserService
from supabase_client import supabase  # Import for role lookup

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def logged_user(request: Request):
    session_token = request.cookies.get('user_session')
    user_service = UserService()
    user = user_service.current_user(session_token)
    if user:
        return user
    else:
        return None

@router.get("/")
def get_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/signup")
def get_signup(request: Request):
    user = logged_user(request)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/login")
def get_login(request: Request):
    user = logged_user(request)
    if user:
        return RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return templates.TemplateResponse("login.html", {"request": request})

@router.post("/api/signup")
def make_signup(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), role: str = Form(...)):
    try:
        user_service = UserService()
        res = user_service.signup_user(email, password, role)
        if res and not getattr(res, 'error', None):
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        else:
            error_msg = getattr(res, 'error', None)
            if error_msg and hasattr(error_msg, 'message'):
                error_msg = error_msg.message
            elif error_msg:
                error_msg = str(error_msg)
            else:
                error_msg = "Signup failed."
            return templates.TemplateResponse("signup.html", {"request": request, "error": error_msg})
    except Exception as e:
        return templates.TemplateResponse("signup.html", {"request": request, "error": str(e)})

@router.post("/api/login")
def make_login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        user_service = UserService()
        res = user_service.login_user(email, password)
        if res and res.session and res.session.access_token:
            access_token = res.session.access_token
            user = user_service.current_user(access_token)
            user_id = user.get("id") if user else None
            role = "user"
            if user_id:
                profile = supabase.table("profiles").select("role").eq("id", user_id).single().execute()
                if profile.data and "role" in profile.data:
                    role = profile.data["role"]
            if role == "company":
                redirect_url = "/company/dashboard"
            else:
                redirect_url = "/user/dashboard"
            response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(
                key="user_session",
                value=access_token,
                httponly=True,
                secure=True,
                samesite='lax',
                max_age=3600
            )
            return response
        else:
            return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    except Exception as e:
        return templates.TemplateResponse("login.html", {"request": request, "error": "login failed."})

@router.get("/dashboard")
def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/user/dashboard")
def get_user_dashboard(request: Request):
    return templates.TemplateResponse("user_dashboard.html", {"request": request})

@router.get("/company/dashboard")
def get_company_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.post("/company/testimonial")
def add_company_testimonial(request: Request, type: str = Form(...), text: str = Form(None), video: UploadFile = Form(None), video_url: str = Form(None)):
    # For demonstration, just print or mock save
    if type == "text" and text:
        print(f"Text testimonial: {text}")
        # Save to DB here
    elif type == "video":
        if video and video.filename:
            print(f"Video file uploaded: {video.filename}")
            # Save file and record to DB here
        elif video_url:
            print(f"YouTube URL: {video_url}")
            # Save URL to DB here
        else:
            return RedirectResponse(url="/company/dashboard?error=Please provide a video file or URL", status_code=303)
    else:
        return RedirectResponse(url="/company/dashboard?error=Invalid testimonial data", status_code=303)
    return RedirectResponse(url="/company/dashboard?success=Testimonial submitted", status_code=303)

@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="user_session")
    return response

@router.post("/api/logout")
def api_logout(request: Request):
    response = JSONResponse({"success": True, "message": "Logged out"})
    response.delete_cookie(key="user_session")
    return response