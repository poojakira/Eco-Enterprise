import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Absolute Reality: File-relative URI resolution
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 1. Path to the CSV Data
    DATA_PATH = os.path.join(BASE_DIR, "data/dpp_data.csv")

    # 2. Path to the Trained Models (MATCHING YOUR TRAINING LOGS)
    MODEL_PATH = os.path.join(BASE_DIR, "data/model.pkl")
    SECURITY_PATH = os.path.join(BASE_DIR, "data/security_model.pkl")

    # 3. Database Configuration (SQLite default, PostgreSQL for Enterprise)
    SQLITE_DB_PATH = os.path.join(os.path.dirname(DATA_PATH), "v7_sustainability.db")
    DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")

    # 4. Security Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", "SUPER_SECRET_KEY_FOR_DEV_ONLY_12345")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

settings = Settings()