from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: Optional[str] = None
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    
    # App
    app_env: str = "development"
    app_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    
    # Weekly Report
    weekly_report_enabled: bool = True
    weekly_report_day: str = "sunday"
    weekly_report_time: str = "20:00"
    
    # Telegram (optional)
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    
    # Email (optional)
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    email_from: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

