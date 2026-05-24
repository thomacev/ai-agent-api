from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str
    
    # Infraestructura
    DATABASE_URL: str
    REDIS_URL: str
    
    # IA
    OPENROUTER_API_KEY: str
    MODEL_NAME: str

    # Cargar archivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
        env_ignore_empty=True,
        )

settings = Settings()