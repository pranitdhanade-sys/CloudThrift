"""Application configuration using environment-driven settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for API, database, and AWS integration."""

    model_config = SettingsConfigDict(env_prefix="CCA_", env_file=".env", extra="ignore")

    app_name: str = "Cloud Cost Optimization Agent"
    environment: str = Field(default="local")
    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/cloudcost")
    aws_region: str = Field(default="us-east-1")


settings = Settings()
