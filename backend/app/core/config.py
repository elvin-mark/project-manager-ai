from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    OLLAMA_API_URL: str = "http://localhost:11434"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = "a_very_secret_key_that_should_be_changed_in_production"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
