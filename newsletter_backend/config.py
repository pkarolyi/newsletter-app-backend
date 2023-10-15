from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(str, Enum):
    prod = "prod"
    dev = "dev"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    env: AppEnv = AppEnv.dev
    port: int
    database_url: str

    session_token_length: int = 32
    session_exp_min: int = 120
    refresh_token_length: int = 64
    refresh_exp_day: int = 30


app_config = AppSettings()
