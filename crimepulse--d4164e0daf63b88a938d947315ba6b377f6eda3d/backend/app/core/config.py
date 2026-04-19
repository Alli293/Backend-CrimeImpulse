"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application Configuration
    app_name: str = "CrimePulse"
    environment: str = "development"
    log_level: str = "info"
    admin_email: str = ""

    # OpenAI Configuration
    openai_api_key: str = ""

    # Langfuse Observability
    langfuse_secret_key: str = ""
    langfuse_public_key: str = ""
    langfuse_host: str = "http://localhost:3000"

    # GenAI Configuration
    genai_api_key: str = ""
    genai_base_url: str = "http://172.18.16.1:8080/v1"
    genai_model: str = "unsloth/Qwen3.5-35B-A3B-GGUF:Q4_K_M"
    llm_temperature: float = 0.7
    llm_top_p: float = 0.95
    llm_presence_penalty: float = 1.5

    # CrimePulse SUPABASE
    supabase_host: str = ""
    supabase_port: str = "5432"
    supabase_password: str = ""
    supabase_database: str = "postgres"
    supabase_user: str = "postgres"

    # Redis/Celery Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_broker_db: int = 1  # Celery broker (task queue)
    redis_backend_db: int = 2  # Celery backend (task results)
    redis_auth: str = ""  # Redis password (optional)

    @property
    def redis_broker_url(self) -> str:
        """Build Redis broker URL for Celery task queue."""
        if self.redis_auth:
            return f"redis://:{self.redis_auth}@{self.redis_host}:{self.redis_port}/{self.redis_broker_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_broker_db}"

    @property
    def redis_backend_url(self) -> str:
        """Build Redis backend URL for Celery task results."""
        if self.redis_auth:
            return f"redis://:{self.redis_auth}@{self.redis_host}:{self.redis_port}/{self.redis_backend_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_backend_db}"


settings = Settings()
