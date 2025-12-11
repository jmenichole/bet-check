"""
Supabase connection and helper utilities

Copyright (c) 2025 Jmenichole
Licensed under MIT License
https://jmenichole.github.io/Portfolio/
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    """Initialize and return Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def verify_connection() -> bool:
    """Verify Supabase connection is working"""
    try:
        client = get_supabase_client()
        response = client.table("factors").select("*").limit(1).execute()
        return True
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return False
