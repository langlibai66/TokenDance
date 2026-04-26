from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

load_dotenv(Path(__file__).parent.parent.parent / ".env")


class Settings(BaseSettings):
    LLM_BASE_URL: str = Field(...)
    LLM_MODEL_NAME: str = Field(...)
    ARK_API_KEY: str = Field(...)


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump_json(indent=2, exclude_none=True))
