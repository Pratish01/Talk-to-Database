import sys
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config import DATABASE_URL

def test_connection():
    """Tests the database connection using the configured DATABASE_URL."""
    print("--- Database Connection Test ---")
    print(f"Testing connection to: {DATABASE_URL}")
    
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("\n[SUCCESS] Successfully connected to the database!")
            print(f"Test query result: {result.scalar()}")
    except Exception as e:
        print("\n[ERROR] Failed to connect to the database.")
        print(f"Error details: {e}")
        print("\nPlease check your DATABASE_URL in the .env file.")
        print("Format: mysql+pymysql://user:password@host:port/database_name")

if __name__ == "__main__":
    load_dotenv()
    test_connection()
