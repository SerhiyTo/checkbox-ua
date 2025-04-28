import os

from fastapi.security import OAuth2PasswordBearer
from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Settings(BaseSettings):
    """
    This class is used to define the settings for the model module.

    Attributes:

    """

    APP_HOST: str = Field("localhost")
    APP_PORT: int = Field(8000)

    DATABASE_URL: PostgresDsn = Field(
        "postgresql://postgres:postgres@localhost:5432/postgres"
    )

    SECRET_KEY: str = Field("secret")
    ALGORITHM: str = Field("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(3600)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )
