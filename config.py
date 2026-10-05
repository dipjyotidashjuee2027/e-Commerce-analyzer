"""
Central place for all configuration values.
Everything is read from environment variables (via a local .env file in
development), so no secrets ever need to be hard-coded or committed.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Google Gemini -----------------------------------------------------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# --- MySQL ---------------------------------------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ecommerce_analytics")

# --- App -------------------------------------------------------------
MAX_ROWS_TO_CHART = 50  # avoid charting huge result sets
QUERY_TIMEOUT_SECONDS = 15
