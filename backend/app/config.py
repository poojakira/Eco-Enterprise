from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from typing import Optional
import os

class Settings(BaseSettings):
    # Core Infrastructure
    PROJECT_NAME: str = "EcoTrack Enterprise"
    VERSION: str = "8.2.0-STABLE"
    ENV: str = os.getenv("ENV", "development")
    
    # Database (Full PostgreSQL Support)
    # Default to production-grade DB if ENV=production
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ecotrack_enterprise.db")
    
    # Security (Hardened)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "industrial_grade_secret_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # ML & Telemetry Nodes
    MODEL_PATH: str = "app/ml/business_intel_v8.joblib"
    SECURITY_PATH: str = "app/ml/security_shield_v8.joblib"
    
    # Observability
    LOG_LEVEL: str = "INFO"
    PROMETHEUS_METRICS: bool = True

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENV', 'development')}",
        env_file_encoding='utf-8',
        case_sensitive=True
    )

settings = Settings()