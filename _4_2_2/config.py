# config.py

from pydantic_settings import BaseSettings

from _4_2_2.schemas import AuthJWT


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
