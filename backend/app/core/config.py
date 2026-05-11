from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "Purna Grocery API"
    API_V1_STR: str = "/api/v1"

    model_config = {"env_file": ".env"}


settings = Settings()
