from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Bicicletos API"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True
    base_url: AnyHttpUrl = Field(..., alias="BASE_URL")
    # Configuración de la base de datos (Database settings)
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_name: str = Field(..., alias="DB_NAME")
    DATABASE_URL: Optional[str] = None

    # Configuración de Auth0 (Auth0 settings)
    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str
    AUTH0_ISSUER: AnyHttpUrl
    AUTH0_ALGORITHMS: str = "RS256"
    AUTH0_ROLES_CLAIM: str
    AUTH0_PERMS_CLAIM: str = "permissions"
    JWKS_CACHE_TTL_SECONDS: int = 600

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def model_post_init(self, __context):
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )

settings = Settings()