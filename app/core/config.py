from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
	AWS_REGION_NAME: str
	DATABASE_URL: str
	JWT_KEY_ID: str
	JWT_SIGNATURE_ALGORITHM: str


	model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# Cache settings to improve performance
@lru_cache
def get_settings():
	return settings

env_vars = get_settings()