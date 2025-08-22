from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    APP_NAME: str = "Bicicletos API"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True


    DATABASE_URL: str


    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str
    AUTH0_ISSUER: AnyHttpUrl
    AUTH0_ALGORITHMS: str = "RS256"
    AUTH0_ROLES_CLAIM: str
    AUTH0_PERMS_CLAIM: str = "permissions"
    JWKS_CACHE_TTL_SECONDS: int = 600


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()