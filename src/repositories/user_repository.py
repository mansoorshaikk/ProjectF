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
    
    def signup_user(self, email, password, role):  # ← Added `role`
        result = self.supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        user_id = result.user.id if result.user else None
        if user_id:
            self.supabase.table("profiles").insert({
                "id": user_id,
                "email": email,
                "role": role
            }).execute()
        return result
    
    def login_user(self, email, password):
        return self.supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    
    def current_user(self, session_token):
        user_response = self.supabase.auth.get_user(session_token)
        
        if not user_response or not getattr(user_response, "user", None):
            return None
        
        user_id = user_response.user.id
        profile = self.supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return profile.data