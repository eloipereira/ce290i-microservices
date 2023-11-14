from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class RedisConfig(BaseSettings):
    redis_host: str
    redis_port: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
