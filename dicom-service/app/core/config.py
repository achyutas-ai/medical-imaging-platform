from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DEFAULT_IMAGE_SIZE: int = 512
    MODEL_PATH: str = "app/models/mock_model.pt"
    OUTPUT_DIR: str = "output/sr"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
