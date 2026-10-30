"""
Application configuration and environment settings.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI-Powered Intelligent Code Review and Software Defect Prediction System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/code_review_db")
    
    # AI settings - Default to ChatGPT API
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")
    AI_API_KEY: str = os.getenv("OPENAI_API_KEY", os.getenv("AI_API_KEY", ""))
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4o-mini")

    # Security & Server
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-production-key-change-me")
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]

settings = Settings()
