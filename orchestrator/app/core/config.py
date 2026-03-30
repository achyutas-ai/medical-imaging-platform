from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    K8S_NAMESPACE: str = "default"
    DICOM_PVC_NAME: str = "dicom-pvc"
    DICOM_MOUNT_PATH: str = "/mnt/dicom"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
