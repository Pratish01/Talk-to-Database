import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project Root
ROOT_DIR = Path(__file__).parent.parent

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    IS_EXTERNAL_DB = True
    # For extraction purposes, we might need a distinct path if it's SQLite, 
    # but for MySQL, the URL is used directly by SQLAlchemy
    DATABASE_PATH = DATABASE_URL 
else:
    DATABASE_PATH = ROOT_DIR / "data" / "company_data.sqlite"
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    IS_EXTERNAL_DB = False

# Vector Store Configuration
VECTORSTORE_DIR = ROOT_DIR / "data" / "faiss_index_v2"

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").lower() # 'openai', 'google', 'groq'

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME")
# Default models based on provider
if not MODEL_NAME:
    if LLM_PROVIDER == "openai":
        MODEL_NAME = "gpt-4o-mini"
    elif LLM_PROVIDER == "google":
        MODEL_NAME = "gemini-2.0-flash"
    elif LLM_PROVIDER == "groq":
        MODEL_NAME = "llama-3.1-70b-versatile"

# Safety Settings
MAX_ROWS_LIMIT = 100
ALLOWED_TABLES = ["employees", "departments", "salaries", "projects"]

# Ensure directories exist
os.makedirs(ROOT_DIR / "data", exist_ok=True)
