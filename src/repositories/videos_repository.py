import os
from supabase import create_client

class VideoRepository:
    def __init__(self):
        SUPABASE_URL = "https://tmqfrqpehwwclkclwkxr.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtcWZycXBlaHd3Y2xrY2x3a3hyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk4OTIxNDQsImV4cCI6MjA2NTQ2ODE0NH0.TSpIVEgkrlRNtrGoO-yGDhemhZNYX7VyMmizS4iVoBE"
        self.supabase = create_client(
            os.getenv("SUPABASE_URL", SUPABASE_URL),
            os.getenv("SUPABASE_KEY", SUPABASE_KEY)
        )
    def upload_files(self,selected_files, user_id):
        """Upload files to Supabase storage and return their URLs."""
        urls = []
        for file in selected_files:
            file_name = f"{user_id}/{file.name}"
            response = self.supabase.storage.from_("videos").upload(file_name, file)
            if response.error:
                print(f"[Error] Failed to upload {file_name}: {response.error.message}")
                continue
            url = self.supabase.storage.from_("videos").get_public_url(file_name)
            urls.append(url.public_url)
        return urls