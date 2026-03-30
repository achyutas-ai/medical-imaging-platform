from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Medical AI Connect Gateway"
    
    # Internal Service URLs
    CONTROL_PLANE_URL: str = "http://localhost:8000"
    ORCHESTRATOR_URL: str = "http://localhost:8001"
    DICOM_SERVICE_URL: str = "http://localhost:8002"
    EDGE_MGMT_URL: str = "http://localhost:8003"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
