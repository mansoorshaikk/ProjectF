import os

from supabase import create_client
from typing import Optional, Dict
from dotenv import load_dotenv


class UserRepository:
    def __init__(self):
        load_dotenv()
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

    def signup_user(self,email,password):
        user = self.supabase.auth.sign_up({"email":email,"password":password})
        return user

    def login_user(self,email,password):
        user = self.supabase.auth.sign_in_with_password({"email":email,"password":password})
        return user

    def current_user(self, session_token):
        user = self.supabase.auth.get_user(session_token)
        return user

