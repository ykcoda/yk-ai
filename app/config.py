import os
from pydantic_settings import BaseSettings, SettingsConfigDict

_model_config = SettingsConfigDict(
    env_file=".env", env_ignore_empty=True, extra="ignore"
)


class AISettings(BaseSettings):
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY") or ""

    model_config = _model_config


ai_settings = AISettings()
