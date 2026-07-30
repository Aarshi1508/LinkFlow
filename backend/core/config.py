"""
Centralized application configuration.

We use pydantic-settings so that:
1. All env vars are validated and typed at startup (fail fast if misconfigured).
2. The rest of the codebase imports `settings` instead of calling os.getenv()
   everywhere, giving us a single source of truth.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "LinkFlow API"
    ENVIRONMENT: str = "development"
    BASE_URL: str = "http://localhost:8000"

    # --- Database ---
    DATABASE_URL: str

    # --- JWT ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- CORS ---
    # Stored as a raw comma-separated string in .env; exposed as a list via
    # the property below so routers/main.py don't need to parse it themselves.
    CORS_ORIGINS: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Single shared instance imported throughout the app.
settings = Settings()
