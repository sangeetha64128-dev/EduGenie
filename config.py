import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    app_name: str = "EduGenie.AI"
    app_version: str = "1.0.0"
    app_description: str = "AI Learning Path"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    local_model_name: str = "MBZUAI/LaMini-Flan-T5-783M"

    class Config:
        env_file = str(ENV_PATH)
        env_file_encoding = "utf-8"
        extra = "allow"

def get_settings():
    return Settings()