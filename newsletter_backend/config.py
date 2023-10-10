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
