# config.py

from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    MODE: Literal['DEV', 'PROD']
    DOCS_USER: str
    DOCS_PASSWORD: SecretStr
