from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Config(BaseSettings):
    api_host: str
    api_port: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
