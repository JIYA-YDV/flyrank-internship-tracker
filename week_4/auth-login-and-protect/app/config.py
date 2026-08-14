# app/config.py
# Supabase client initialization.
# This is the ONLY file that reads your secrets and creates the client.
# Every other file imports `supabase` from here — never from .env directly.

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env file into environment variables
# Must happen before we read os.environ below
load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY", "")

# Fail fast at startup — better to crash immediately than run misconfigured.
# If either secret is missing, the server stops before accepting any request.
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "❌  SUPABASE_URL and SUPABASE_KEY must be set in your .env file.\n"
        "    Copy .env.example to .env and fill in your Supabase project values."
    )

# We use the anon (public) key here.
# NEVER use the service_role key in your app — it bypasses Row Level Security
# and gives unrestricted access to your entire database.
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("✅  Supabase client initialized successfully")