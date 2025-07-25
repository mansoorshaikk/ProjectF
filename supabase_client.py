from supabase import create_client, Client

url = "https://tmqfrqpehwwclkclwkxr.supabase.co"

key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRtcWZycXBlaHd3Y2xrY2x3a3hyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk4OTIxNDQsImV4cCI6MjA2NTQ2ODE0NH0.TSpIVEgkrlRNtrGoO-yGDhemhZNYX7VyMmizS4iVoBE"

supabase: Client = create_client(url, key)
