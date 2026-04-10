"""Configuration management using Pydantic and python-dotenv."""

import os
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Google ADK
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    google_adk_model: str = Field(default="gemini-2.5-flash", alias="GOOGLE_ADK_MODEL")

    # OpenSandbox
    sandbox_api_key: str = Field(default="", alias="SANDBOX_API_KEY")
    sandbox_domain: str = Field(
        default="sandboxes.resultcrafter.com",
        alias="SANDBOX_DOMAIN",
    )
    sandbox_image: str = Field(
        default="sandbox-registry.cn-zhangjiakou.cr.aliyuncs.com/opensandbox/code-interpreter:v1.0.2",
        alias="SANDBOX_IMAGE",
    )

    # Output
    audit_output_dir: str = Field(default="/workspace", alias="AUDIT_OUTPUT_DIR")

    def validate(self) -> None:
        """Validate required settings."""
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required")
        if not self.sandbox_api_key:
            raise ValueError("SANDBOX_API_KEY is required")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()
