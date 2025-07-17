from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    OLLAMA_API_URL: str = "http://localhost:11434"
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"


settings = Settings()
