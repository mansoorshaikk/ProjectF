import os

from supabase import create_client
from typing import Optional, Dict
from dotenv import load_dotenv

import os
from supabase import create_client

class UserRepository:
    def __init__(self):
        
        SUPABASE_URL = "https://tmqfrqpehwwclkclwkxr.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtcWZycXBlaHd3Y2xrY2x3a3hyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk4OTIxNDQsImV4cCI6MjA2NTQ2ODE0NH0.TSpIVEgkrlRNtrGoO-yGDhemhZNYX7VyMmizS4iVoBE"

        
        self.supabase = create_client(
            os.getenv("SUPABASE_URL", SUPABASE_URL),
            os.getenv("SUPABASE_KEY", SUPABASE_KEY)
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

