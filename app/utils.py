import os
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


_model_config = SettingsConfigDict(
    env_file=".env", env_ignore_empty=True, extra="ignore"
)


class AISettings(BaseSettings):
    OPENAI_API_KEY: SecretStr = SecretStr(os.getenv("OPENAI_API_KEY") or "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL") or ""
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL") or ""

    model_config = _model_config
    model_config = _model_config


ai_settings = AISettings()
