from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Sistema
    ENVIRONMENT: str = Field(default="development")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=False)

    # Bot Telegram
    TELEGRAM_BOT_TOKEN: str

    # IA (Google Gemini)
    GOOGLE_GEMINI_API_KEY: str
    
    # IA (Outras - para fallback futuro)
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # Banco de Dados (Supabase)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None

    # Mercado Livre (OAuth)
    MERCADO_LIVRE_APP_ID: Optional[str] = None
    MERCADO_LIVRE_CLIENT_SECRET: Optional[str] = None
    MERCADO_LIVRE_REDIRECT_URI: Optional[str] = None

settings = Settings()
