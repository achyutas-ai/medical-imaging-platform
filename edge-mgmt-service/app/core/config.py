from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    EDGE_HOST: str = "192.168.1.50"
    EDGE_USER: str = "ubuntu"
    EDGE_KEY_PATH: str = "~/.ssh/id_rsa"
    VM_NAME: str = "medical-inference-vm"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
