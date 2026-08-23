"""
This file reads settings (like the database link and secret key) from a
.env file instead of writing them directly in the code. This is important
so we never accidentally upload passwords or API keys to GitHub.
"""

import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Fail loudly at startup if something important is missing,
# instead of failing later in a confusing way.
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Did you create a .env file?")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing. Did you create a .env file?")
