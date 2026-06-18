# Central Configuration Loader
# Reads all values from .env file
from pathlib import Path
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = Field(default="AI Enterprise Policy Assistant")
    app_version: str = Field(default="1.0.0")
    app_env: str = Field(default="development")
    debug: bool = Field(default=True)

    mistral_api_key: str = Field(default="", alias="MISTRAL_API_KEY")
    mistral_model_large: str = Field(default="mistral-large-latest", alias="MISTRAL_MODEL_LARGE")
    mistral_model_small: str = Field(default="mistral-small-latest", alias="MISTRAL_MODEL_SMALL")

    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)

    jwt_secret_key: str = Field(default="enterprise_secret_key_2026")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expire_minutes: int = Field(default=60)

    database_url: str = Field(default="mysql+pymysql://root:root@localhost:3306/enterprise_policy_db")
    db_host: str = Field(default="localhost")
    db_port: int = Field(default=3306)
    db_name: str = Field(default="enterprise_policy_db")
    db_user: str = Field(default="root")
    db_password: str = Field(default="root")

    chroma_db_path: str = Field(default="./data/chroma_db")
    chroma_collection_name: str = Field(default="enterprise_policies")
    policy_docs_path: str = Field(default="./data/policies")
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="./logs/app.log")

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()