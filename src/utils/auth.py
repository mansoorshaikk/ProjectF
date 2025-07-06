from fastapi import Request
from typing import Optional

def get_logged_in_user(request: Request) -> Optional[str]:
    """
    Tries to read the logged-in user from a cookie.
    Returns user email or None if not authenticated.
    """
    user_email = request.cookies.get("user_email")
    return user_email if user_email else None
