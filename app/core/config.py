from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal


class Settings(BaseSettings):
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")
    ADMIN_ID: int = Field(..., env="ADMIN_ID")
    PAYMENT_WALLET: str = Field(..., env="PAYMENT_WALLET")

    ENV: Literal["development", "production"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    DATABASE_URL: str = "sqlite+aiosqlite:///./forgealpha.db"

    # Tier configuration
    TIER_DELAYS: dict[int, int] = {0: 60, 1: 30, 2: 5, 3: 0}
    TIER_PRICES: dict[int, float] = {0: 0, 1: 100, 2: 150, 3: 0}

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()