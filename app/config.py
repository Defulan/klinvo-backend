from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    COOKIE_KEY: str

    FRONTEND_URL: str
    DATABASE_URL: str = "sqlite:///../data.db"

    COOKIE_SECURE: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
