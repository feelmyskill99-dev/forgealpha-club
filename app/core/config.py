from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "development"
    BOT_TOKEN: str
    ADMIN_ID: int
    PAYMENT_WALLET: str

    DATABASE_URL: str = "forgealpha.db"
    LOG_LEVEL: str = "INFO"

    BASIC_DELAY_SECONDS: int = 900
    VIP_DELAY_SECONDS: int = 0

    BASIC_PRICE_USD: int = 49
    VIP_PRICE_USD: int = 149

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def TIER_PRICES(self) -> dict[int, int]:
        return {
            1: self.BASIC_PRICE_USD,
            2: self.VIP_PRICE_USD,
        }

    @property
    def TIER_DELAYS(self) -> dict[int, int]:
        return {
            1: self.BASIC_DELAY_SECONDS,
            2: self.VIP_DELAY_SECONDS,
        }


settings = Settings()  # type: ignore[call-arg]
